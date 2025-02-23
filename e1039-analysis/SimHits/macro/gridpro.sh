do_emul="false"
ido_MC_embedding="false"
do_data_embedding="false"
<<COMMENT
./gridsub.sh mu-_std_original_Kun_P standard mu- $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub.sh mu+_std_original_Kun_P standard mu+ $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub.sh JPsi_std_original_Kun_P standard JPsi $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub_upgrade_sagitta.sh m0_mu-_std_upgradeKun_P standard mu- $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub_upgrade_sagitta.sh m0_mu+_std_upgradeKun_P standard mu+ $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub_upgrade_sagitta.sh m0_JPsi_std_upgradeKun_P standard JPsi $do_emul $do_MC_embedding $do_data_embedding 1000 1930 0 -300 600 1000
./gridsub_upgrade_sagitta.sh m100_mu-_std_upgradeKun_P standard mu- $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -100 -300 600 1000
./gridsub_upgrade_sagitta.sh m100_mu+_std_upgradeKun_P standard mu+ $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -100 -300 600 1000
./gridsub_upgrade_sagitta.sh m100_JPsi_std_upgradeKun_P standard JPsi $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -100 -300 600 1000
./gridsub_upgrade_sagitta.sh m200_mu-_std_upgradeKun_P standard mu- $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -200 -300 600 1000
./gridsub_upgrade_sagitta.sh m200_mu+_std_upgradeKun_P standard mu+ $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -200 -300 600 1000
./gridsub_upgrade_sagitta.sh m200_JPsi_std_upgradeKun_P standard JPsi $do_emul $do_MC_embedding $do_data_embedding 1000 1930 -200 -300 600 1000

