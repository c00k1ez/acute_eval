conda activate parlai_env

mephisto register mturk \
        name=MynaLabs \
        access_key_id=$ACCESS_KEY \
        secret_access_key=$SECRET_KEY

mephisto register mturk_sandbox \
        name=MynaLabs_sandbox \
        access_key_id=$ACCESS_KEY \
        secret_access_key=$SECRET_KEY


if [ -d "./logs/" ] 
then
    echo "logs dir already exists" 
else
    mkdir logs
fi

mephisto config core.main_data_directory ~/Documents/acute_eval/logs

python  fast_eval.py mephisto.blueprint.config_path=$(pwd)/task_config/model_config_logs.json \
	mephisto.provider.requester_name=MynaLabs

