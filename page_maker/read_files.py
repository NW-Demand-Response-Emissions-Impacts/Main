import pandas as pd

def get_impacts(url, bin_types, bin_numbers, seasons):

    impacts = {}
    for i in range(len(bin_types)):
        for j in range(len(bin_numbers)):
            for k in range(len(seasons)):
                if (bin_types[i]=='newbins' and bin_numbers[j]!='Bin_1') or (bin_types[i]=='oldbins' and seasons[k]=='Fall'):
                    pass
                else:
                    impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]] = pd.read_csv(url+'/emissions_impacts/'+bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'.csv?raw=True')

                    impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_cumulative'] = impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]].sum()
                if (bin_types[i] == 'newbins' and bin_numbers[j] == 'Bin_1'):
                    impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_total'] = impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_cumulative']['DVR'] + impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_cumulative']['ResTOU_shed']
                elif (bin_types[i] == 'oldbins' and seasons[k]!='Fall'):
                    impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_total'] = impacts[bin_types[i]+'_'+bin_numbers[j]+'_'+seasons[k]+'_cumulative'][2::].sum()

    return impacts

def get_rates_drdays(url, bin_types, seasons, scenarios):

    rates = {}
    for i in range(len(bin_types)):
        for j in range(len(seasons)):
            for k in range(len(scenarios)):
                if (bin_types[i]=='oldbins' and seasons[j]=='Fall'):
                    pass
                else:
                    rates[bin_types[i]+'_'+seasons[j]+'_'+scenarios[k]] = pd.read_csv(url+'/emissions_rates/DRdays_allyears_'+bin_types[i]+'_'+seasons[j]+'_'+scenarios[k]+'.csv?raw=True')

    return rates

def get_rates_alldays(url, seasons, scenarios):

    rates = {}
    for i in range(len(seasons)):
        for j in range(len(scenarios)):
            rates[seasons[i]+'_'+scenarios[j]] = pd.read_csv(url+'/emissions_rates/alldays_2022_'+seasons[i]+'_'+scenarios[j]+'.csv?raw=True')

    return rates

def get_potential(url, bin_types, seasons, bin_numbers):

    potential = {}
    potential['comparison_barchart'] = pd.read_csv(url+'/dr_potential/comparison_barchart.csv?raw=True')
    potential['dr_hours'] = pd.read_csv(url+'/dr_hours/output_dr_hours.csv?raw=True')
    for i in range(len(bin_types)):
        for j in range(len(seasons)):
            for k in range(len(bin_numbers)):
                if (bin_types[i]=='newbins' and bin_numbers[k]!='bin1') or (bin_types[i]=='oldbins' and seasons[j]=='Fall'):
                    pass
                else:
                    potential[bin_types[i]+'_'+seasons[j]+'_'+bin_numbers[k]] = pd.read_csv(url+'/dr_potential/'+bin_types[i]+'_'+seasons[j]+'_'+bin_numbers[k]+'.csv?raw=True')

    return potential