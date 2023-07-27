!#/bin/bash

FILE=../Experiment_results/exp1.txt
if [ -f "$FILE" ]; then
    rm $FILE
else
    touch $FILE
fi

cd ..

LEN=20
for i in {50..250}
do
    for j in {1..20}
    do
    python3 sim.py \
--exp_no 1 \
--input_duration 200 \
--sim_len 200 \
--num_reqs $i \
--network_delay 2 \
--load AUTO \
--issue_failures 1 \
--issue_mitigations 1 \
--plot_dropped 0 \
--plot_receive_dropped 0 \
--plot_pending_dropped 0 \
--plot_served 0 \
--plot_responded 0 \
--plot_retried 0 \
--plot_failures 0 \
--plot_mitigations 0 \
--plot_service_dropped 0 \
--plot_enabled 0
    done
done

cd Experiments
python3 plot_exp1.py --avg_len $LEN