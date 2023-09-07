!#/bin/bash

python3 sim.py \
--exp_no 0 \
--input_duration 200 \
--sim_len 200 \
--num_reqs 200 \
--network_delay 2 \
--load LOAD_SHOCK \
--issue_failures 0 \
--issue_mitigations 1 \
--plot_dropped 0 \
--plot_receive_dropped 0 \
--plot_pending_dropped 0 \
--plot_served 0 \
--plot_responded 1 \
--plot_retried 1 \
--plot_failures 1 \
--plot_mitigations 1 \
--plot_service_dropped 1 \
--plot_enabled 1 \
--monitor_policy HEART_BEAT \
--monitor_frequency 7\