#! bin bash -l

dir="sbatch_log"
job_File="sbatch_run.sh" 
dataset=$"COVID19_Xray"

for epochs in 100 200 300
do
    for batch in 128 256
    do 
        for lr in 0.001 0.0001 0.0003
        do 
            for version in 1 2
            do
                EXPT=simclr_COVID19_Xray_"$lr"_"$batch"_"$epochs"_"$version"
                STD=$dir/STD_simclr_COVID19_Xray_"$lr"_"$batch"_"$epochs"_"$version".out
                ERR=$dir/ERR_simclr_COVID19_Xray_"$lr"_"$batch"_"$epochs"_"$version".err
                export lr;
                export batch;
                export epochs;
                export version;
                sbatch -J $EXPT -o $STD -t 00-23:00:00 -e $ERR $job_File
            done;
        done;
    done;
done;
