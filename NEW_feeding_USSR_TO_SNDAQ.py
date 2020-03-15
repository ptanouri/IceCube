""" Python script to run sni3_sn_sim using subprocess """

import os
import sys
import subprocess
import errno
import numpy

def mkdir_p(path):
    """ mkdir -p """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            print(path)
        else:
            raise

def main():
    """ Main.
    Run sni3_sn_sim. Parameters required:
        1: SnFile                      : TODO-add comment
        2: DstFile                     : TODO-add comment
        3: USSR file                   : Preprocessed simulations output from USSR
        4: use signal sim              : TODO-add comment
        5: save dir                    : Output directory
        6: prefix string               : TODO-add comment
        7: star distri                 : Star distribution
        8: sn distance                 : Distance to supernova (maximum !!!!!?)
        9: use muon subtraction        : Option to subtract muon from signal.
        10: file for V_eff (normal QE) : Effective volume of normal Doms given ice model.
        11: file for V_eff (high QE)   : Effective volume of DeepCore Doms given ice model.
    """
    # User-defined parameters
    snd_min = float(sys.argv[1])
    snd_max = float(sys.argv[2])
    snd_step = float(sys.argv[3])
    run_per_snd = int(sys.argv[4])

    # Define path
    ussr_dir = "/home/pooyah/Documents/USSR/tribranch"
    sndaq_dir = "/home/pooyah/Beer_Trooper_CMake"

    # Define arguments
    sn_file = "/home/pooyah/Beer_Trooper_CMake/build/sndata_121502_000_2013.root"
    dst_file = "no_dst_data"
    ussr_file = ussr_dir + "/preprocessed_simulations/sn_model_10_spectrum_10_hierarchy_inverted_sqsin2theta_0.000001_collective_0_star_1_shocks_0_vaccuum_0_earth_0_invert_cs_0_inv_beta_1_e_scat_1_O16CC_1_O16NC_1_O18_1_nu_angle_0_energy_0MeV_to_100MeV_in_0.1MeV_steps_time_0.0001s_resolution.root"
    signal_sim = 1
    save_dir = sndaq_dir + "/output(1-20-2-1)/"  # This NEEDS to end in /. DON'T QUESTION IT
    star_dist = 1
    distance = numpy.arange(snd_min, snd_max + snd_step, snd_step)
    muon = 0
    veff = "effectivevolume_benedikt_AHA_normalDoms.txt"
    veff_dc = "effectivevolume_benedikt_AHA_DeepCoreDoms.txt"

    # Make sure folder exists
    mkdir_p(save_dir+"new")
    mkdir_p(save_dir+"signals")
    mkdir_p(save_dir+"debug")
    mkdir_p(save_dir+"original")

    # Run sni3_sn_sim
    for snd in distance:
        for num in range(run_per_snd):
            prefix = "BH_IH_{0:02.1f}kpc_{1:04d}".format(snd,num)
            subprocess.call("{}/install/bin/sni3_sn_sim {} {} {} {} {} {} {} {} {} {} {}".format(sndaq_dir, sn_file, dst_file, ussr_file, signal_sim, save_dir, prefix, star_dist, snd, muon, veff, veff_dc).split())

if __name__ == "__main__":
    main()

