from NoisePreProcess import *
from Plots import *
import os


def main():
    #Define your Thresholds
    # thresholds_list = [55,60,65]
    thresholds_list = [55,56,57,58,59,60,61,62,53,64,65]
    LA = {
        'City_noise_files': [
            ['LARawDat/Cumulative_TR_LA_1000ft.csv', 'Medium'],
            ['LARawDat/Cumulative_High_Freq_TR_LA_1000ft.csv', 'High']
        ],
        'struct_list': [
            pd.read_csv('LARawDat/Schools_Colleges_and_Universities.csv'),
            pd.read_csv('LARawDat/Churches.csv'),
            pd.read_csv('LARawDat/Hospitals_and_Medical_Centers.csv')
        ],
        'City_density': 0.0004374008748, #defined by mic denisty in RCAIDE
        'City_bounds': Polygon([(-118.5, 33.6), (-117.85, 33.6), (-117.85, 34.4), (-118.5, 34.4)]),
        'City_geojson': 'LARawDat/LABG_Merged.geojson',
        'frequency': ['Medium', 'High'],
        'ambient_noise': 'LARawDat/LA_Aviation_Modes.csv'}


    DFW = {
        'City_noise_files': [
            ['DFWRawData/Cumulative_TR_DFW_1000ft.csv', 'Medium'],
            ['DFWRawData/Cumulative_High_Freq_TR_DFW_1000ft.csv', 'High']],

        'struct_list': [
            pd.read_csv('DFWRawData/Texas Schools.csv'),
            pd.read_csv('DFWRawData/Churches.csv'),
            pd.read_csv('DFWRawData/Hospitals.csv')],

        'City_density': 0.0002263142014, #defined by mic denisty in RCAIDE
        'City_bounds': Polygon([(-97.3, 32.6), (-96.5, 32.6), (-96.5, 33.3), (-97.3, 33.3)]),
        'City_geojson': 'DFWRawData/DFWHousing.geojson',
        'frequency': ['Medium', 'High'],
        'ambient_noise': 'DFWRawData/TX_Aviation_Modes.csv'}

    cities = {'LA': LA,'DFW':DFW}

    for city, config in cities.items():
        data_save_path = f'Final_{city}_Data'
        plot_save_path = f'{city}_Plots'
        frequency = config['frequency']
        City_density = config['City_density']
        City_geojson = config['City_geojson']
        City_bounds = config['City_bounds']
        ambient_noise = config['ambient_noise']
        City_noise_files = config['City_noise_files']
        struct_list = config['struct_list']
        os.makedirs(data_save_path, exist_ok=True)
        os.makedirs(plot_save_path, exist_ok=True)



        all_results = []        
        for i, (noise_file, freq_label) in enumerate(City_noise_files):
            for j, threshold in enumerate(thresholds_list):
                unique_pts = difference_noise_pts(
                    dot_noise_file=ambient_noise,
                    leads_noise_file=noise_file, 
                    threshold=threshold)

                City = process_unique_research_noise(
                    census_tracts_gdf=City_geojson,
                    unique_noise_gdf=unique_pts,
                    output_prefix=f'Final_{city}_Data/{city}_{threshold}_{freq_label}')

                res = struct_in_contours(
                    geojson=City_geojson,
                    dot_noise_file=ambient_noise,
                    leads_noise_file=noise_file,
                    sens_struct_list=struct_list,
                    city=city,
                    p_bounds=City_bounds,
                    threshold=threshold,
                    frequency=freq_label)

                all_results.append(res)

        city_final = pd.concat(all_results, ignore_index=True)
        # thresholds_list = [55,60,65]
        # noise Costs
        Noise_files = []
        for j,_ in enumerate(thresholds_list):
            for k,freq in enumerate(frequency):
                # print(f'{data_save_path}/{city}_{thresholds_list[j]}_{freq}_Noise.csv')
                Noise_files.append(pd.read_csv(f'{data_save_path}/{city}_{thresholds_list[j]}_{freq}_Noise.csv'))

        Noise_files_paths = []
        Noise_files_dfs = []
        city_operations = {freq: [] for freq in frequency} 

        for j, threshold in enumerate(thresholds_list):
            for k, freq in enumerate(frequency):
                path = f'{data_save_path}/{city}_{threshold}_{freq}_Noise.csv'
                Noise_files_paths.append(path)
                Noise_files_dfs.append(pd.read_csv(path))

        #Homes Impacted and Cost
        Homes_impacted = []
        Homes_cost = []
        Homes_cost_error =[]

        COST_PER_HOUSEHOLD = 57093.41 / 1e6
        COST_PER_HOUSEHOLD_error = 5347.707817 / 1e6

        full_city_cost_dfs = []

        for path, file in zip(Noise_files_paths, Noise_files_dfs):
            compute_single_households(file)
            impacted = compute_impacted(file, City_density)
            Homes_impacted.append(impacted)
            Homes_cost.append(impacted * COST_PER_HOUSEHOLD)
            Homes_cost_error.append(impacted * COST_PER_HOUSEHOLD_error)
            city_operations[freq].append(impacted)

            # Extract threshold and frequency from filename
            parts = path.split('/')[-1].replace('.csv','').split('_')
            threshold = int(parts[1])
            freq = parts[2]

            city_cost_df = pd.DataFrame({
                'Threshold (dBA)': [threshold],
                'Cost (Millions $)': [impacted * COST_PER_HOUSEHOLD],
                'Error (Millions $)': [impacted * COST_PER_HOUSEHOLD_error],
                'Operation Freq': [freq]})
            

            full_city_cost_dfs.append(city_cost_df)


        full_city_cost_df = pd.concat(full_city_cost_dfs, ignore_index=True)

        
        #save CSV Data
        city_final.to_csv(f'{data_save_path}/AllStructStatistics_{city}.csv', index=False)
        full_city_cost_df.to_csv(f'{plot_save_path}/Cost_{city}_Results.csv', index=False)


        #plotting
        struct_stats_barplot(f'{data_save_path}/AllStructStatistics_{city}.csv', city)
        city_costs_list = [city_operations[freq] for freq in frequency]
        plot_homes_impacted(thresholds_list, city_costs_list, frequency, f'{plot_save_path}/{city}_Homes_Impacted.png')

    return


if __name__ == "__main__":
    main()