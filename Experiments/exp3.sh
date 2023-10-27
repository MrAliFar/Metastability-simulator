!#/bin/bash
!#/bin/bash

FILE=../Experiment_results/exp4.txt
if [ -f "$FILE" ]; then
    rm $FILE
else
    touch $FILE
fi

cd ..


for j in {6..20}
do
    python3 change_config1.py \
--default_load 3 \
--spike_load $j 

        for k in {1..10}
        do
        python3 sim.py \
--exp_no 4 \
--input_duration 200 \
--sim_len 200 \
--num_reqs 200 \
--network_delay 2 \
--load LOAD_SHOCK \
--issue_failures 0 \
--issue_mitigations 0 \
--plot_dropped 0 \
--plot_receive_dropped 0 \
--plot_pending_dropped 0 \
--plot_served 0 \
--plot_responded 1 \
--plot_retried 1 \
--plot_failures 0 \
--plot_mitigations 0 \
--plot_service_dropped 0 \
--plot_enabled 0 \
--monitor_policy HEART_BEAT \
--monitor_frequency 5 \
--garbage_collect 0 \
--controller 0 
    done
done


for j in {6..20}
do
python3 change_config1.py \
--default_load 3 \
--spike_load $j 

    for k in {1..10}
    do
    python3 sim.py \
--exp_no 4 \
--input_duration 200 \
--sim_len 200 \
--num_reqs 200 \
--network_delay 2 \
--load LOAD_SHOCK \
--issue_failures 0 \
--issue_mitigations 0 \
--plot_dropped 0 \
--plot_receive_dropped 0 \
--plot_pending_dropped 0 \
--plot_served 0 \
--plot_responded 1 \
--plot_retried 1 \
--plot_failures 0 \
--plot_mitigations 0 \
--plot_service_dropped 0 \
--plot_enabled 0 \
--monitor_policy HEART_BEAT \
--monitor_frequency 5 \
--garbage_collect 0 \
--controller 2
    done
done

