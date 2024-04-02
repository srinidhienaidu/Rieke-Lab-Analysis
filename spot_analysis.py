import numpy as np
def type_psth_by_intensity(spike_dict: dict, d_main_IDs: dict, 
                               spot_intensity: np.ndarray, str_type: str='OnP'):
    """
    Inputs: 
    spike_dict: keys cell IDs, fr values in [n_epochs x n_bins]
    str_type: cell type label
    d_main_IDs: keys are cell type labels, values are list of Cell IDs of that type
    spot_intensity: intensity values in [n_epochs]

    Output: 
    fr in [n_cells, n_unique_intensities, n_bins]
    """

    # Keep only ids that are keys in spike_dict
    sd_ids = list(spike_dict.keys())
    type_ids = d_main_IDs[str_type]
    type_ids = np.intersect1d(sd_ids, type_ids)


    n_unique = np.unique(spot_intensity).shape[0]
    n_epochs = spot_intensity.shape[0]

    if n_epochs != spike_dict[type_ids[0]].shape[0]:
        print('N_epochs dont match!!!')


    n_bins = spike_dict[type_ids[0]].shape[1]
    n_cells = len(type_ids)


    type_psth = np.zeros((n_cells, n_unique, n_bins))
    for idx_id, n_id in enumerate(type_ids):
        all_psth = spike_dict[n_id]
        for idx_flash, flash in enumerate(np.unique(spot_intensity)):
            epoch_idx = np.where(spot_intensity==flash)[0]
            psth_flash = all_psth[epoch_idx]
            avg_psth_flash = psth_flash.mean(axis=0)

            type_psth[idx_id, idx_flash, :] = avg_psth_flash
            
        
    return type_psth