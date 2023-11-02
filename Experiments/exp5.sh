!#/bin/bash
!#/bin/bash

FILE=../Experiment_results/exp9.txt
if [ -f "$FILE" ]; then
    rm $FILE
else
    touch $FILE
fi

cd ..

for i in {2..10}
do
    for j in {2..16}
    do
        python3 change_config1.py \
--default_load $i \
--spike_load $j 

        for k in {1..20}
        do
        python3 sim.py \
--exp_no 9 \
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
--garbage_collect 1 \
--controller 0  
        done
    done
done

for i in {2..10}
do
    for j in {2..16}
    do
    python3 change_config1.py \
--default_load $i \
--spike_load $j 

        for k in {1..20}
        do
        python3 sim.py \
--exp_no 9 \
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
--controller 4
        done
    done
done

