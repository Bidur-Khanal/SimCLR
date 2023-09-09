#! bin bash -l

dir="sbatch_log"
job_File="sbatch_run.sh" 
dataset=$"mura"
epochs=$"300"
batch=$"128"


for lr in 0.001 0.01
do 
    for version in 1 2
    do
        EXPT=simclr_mura_"$lr"_"$batch"_"$epochs"_"$version"
        STD=$dir/STD_simclr_mura_"$lr"_"$batch"_"$epochs"_"$version".out
        ERR=$dir/ERR_simclr_mura_"$lr"_"$batch"_"$epochs"_"$version".err
        export lr;
        export batch;
        export epochs;
        export version;
        export dataset;
        sbatch -J $EXPT -o $STD -t 01-05:00:00 -e $ERR $job_File
    done;
done;

