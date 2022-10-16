#!/bin/bash
[[ -z "${SPARK_ACTION}" ]] && { echo "SPARK_ACTION required"; exit 1; }

# ACTIONS start-zk, start-kafka, create-topic, 

echo "Running action ${SPARK_ACTION}"
case ${SPARK_ACTION} in
"example")
echo "Running example ARGS $@"
./bin/run-example $@
;;
"spark-shell")
./bin/spark-shell --master local[2]
;;
"pyspark")
./bin/pyspark --master local[2]
;;
"spark-submit-python")
cd bin
spark-submit --packages $2 /opt/tap/$1
;;
"spark-submit-apps")
 ./bin/spark-submit --packages $3 --class $1 /opt/tap/apps/$2
;;
"pytap")
cd bin
#ls
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.3.0 spark-manager #spark-manager non va bene, gli devo mettere un file con un main (quindi forse devo trovare il mio script di python e mettergli un main)
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.3.0 ../../../opt/tap/${TAP_CODE}
cd ../
cd /opt/tap/
#python ${TAP_CODE}
#python3 ${TAP_CODE}
;;
"bash")
while true
do
	echo "Keep Alive"
	sleep 10
done
;;
esac

