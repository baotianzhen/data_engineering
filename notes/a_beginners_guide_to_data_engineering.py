# https://medium.com/@rchang/a-beginners-guide-to-data-engineering-part-ii-47c4e7cbda71
'''
OPERATORS: Sensors, Operators, and Transfers

    Sensors
        waits for a certain time, external file,
        or upstream data source

        unblock the data flow after a certain time
        has passed or when data from an upstream
        data source becomes available


    Operators
        triggers a certain action (e.g. run a bash
        command, execute a python function, or
        execute a Hive query)

        trigger data transformations, which corresponds
        to the *Transform* step.

        at Airbnb, the most common operator used
        is HiveOperator (to execute Hive operations),
        but they also use PythonOperator (e.g. to run a
        Python script) and BashOperator (e.g. to run
        a bash script, or even a Spark job)


    Transfers
        moves data from one location to another

        often maps to the Load step in ETL

        Airbnb uses MySqlToHiveTransfer or
        S3ToHiveTransfer pretty often, but this
        largely depends on one's data infrastructure
        and where the data warehouse lives

'''

'''
A DAG docstring might be a good way to explain at a high level
what problem space the DAG is looking at.
Links to design documents, upstream dependencies etc
are highly recommended.
'''
from datetime import datetime, timedelta
from airflow.models import DAG # Import the DAG class
from airflow.operators.sensors import NamedHivePartitionSensor
from airflow.operators.hive_operator import HiveOperator

### You can import more operators as you see fit!
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator

# setting some default arguments for the DAG
default_args = {
        'owner': 'you',
        'depends_on_past': False,
        'start_date': datetime(2018, 2, 9),
        }

# Instantiate the Airflow DAG
dag = DAG(
        dag_id='anatomy_of_a_dag',
        description="This describes my DAG",
        default_args=default_args,
        schedule_interval=timedelta(days=1)) # This is a daily DAG

# Put upstream dependencies in a dictionary
wf_dependencies = {
        'wf_upstream_table_1': 'upstream_table_1/ds={{ ds }}',
        'wf_upstream_table_2': 'upstream_table_2/ds={{ ds }}',
        'wf_upstream_table_3': 'upstream_table_3/ds={{ ds }}',
        }

# Define the sensors for upstream dependencies
for wf_task_id, partition_name in wf_dependencies.iteritems():
    NamedHivePartitionSensor(
            task_id=wf_task_id,
            partition_names=[partition_name],
            dag=dag
            )

# Put the tasks in a list
tasks = [
        ('hql', 'task_1'),
        ('hql', 'task_2'),
        ]

# Define operators in the list above
for directory, task_name in tasks:
    HiveOperator(
            task_id=task_name,
            hql='{0}/{1}.hql'.format(directory, task_name),
            dag=dag,
            )

# Put dependencies in a map
deps = {
        'task_1':[
            'wf_upstream_1',
            'wf_upstream_2',
            ],
        'task_2':[
            'wf_upstream_1',
            'wf_upstream_2',
            'wf_upstream_3',
            ],
        }

# Explicitly define the dependencies in the DAG
for downstream, upstream_list in deps.iteritems():
    for upstream in upstream_list:
        dag.set_dependency(upstream, downstream)

'''
Principles of a Good ETL Pipeline:
    - Partition data tables
        Data partitioning can be especially useful
        when dealing with large-size tables with a
        long history. When data is partitioned using
        datestamps, we can leverage dynamic partions
        to parallelize backfilling.

            CREATE TABLE IF NOT EXISTS fct_bookings(
                    id_listing BIGINT COMMENT 'Unique ID of the listing'
                  , id_host    BIGINT COMMENT 'Unique ID of the host who owns the listing'
                  , m_bookings BIGINT COMMENT 'Denoted 1 if a booking transaction occurred'
                )
                PARTITION BY ( -- this is how we define partion keys
                    ds STRING
                );

    - Load data incrementally
        This makes your ETL more modular and manageable,
        especially when building dimension tables from
        the fact tables. In each run, we only need to
        append the new transactions to the dimension
        table from previous date partition instead of
        scanning the entire fact history.

        **Not Recommended Approach: Scan the entire table and rebuild everyday**
            INSERT OVERWRITE TABLE dim_total_bookings PARTITION (ds = '{{ ds }}')
            SELECT
                dim_market
              , SUM(m_bookings) AS m_bookings
            FROM
                fct_bookings
            WHERE
                ds <= '{{ ds }}' -- this is expensive, and can quickly run into scale issues
            GROUP BY
                dim_market
            ;

        **Recommended Approach: Incremental Load**
            INSERT OVERWRITE TABLE dim_total_bookings PARTITION (ds = '{{ ds }}')
            SELECT
                dim_market
              , SUM(m_bookings) AS m_bookings
            FROM (
                SELECT
                    dim_market
                  , m_bookings
                FROM
                    dim_total_bookings      --a dim table
                WHERE
                    ds = DATE_SUB('{{ ds }}', 1)  --from the previous ds

                UNION

                SELECT
                    dim_market
                  , SUM(m_bookings) AS m_bookings
                FROM
                    fct_bookings            -- a fct table
                WHERE
                    ds = '{{ ds }}'         -- from the current ds
                GROUP BY
                    dim_market
            ) a
            GROUP BY
                dim_market
            ;

    - Enforce idempotency
        Many data scientists rely on point-in-time
        snapshots to perform historical analysis.
        This means the underlying source table should
        not be mutable as time progresses, otherwise
        we would get a different answer. Pipeline
        should be built so that the same query,
        when run against the same business logic
        and time range, returns the same result.
        This property has a fancy name called
        Idempotency.

    - Paramaterize workflow
        Just like how templates greatly simplified
        the organization of HTML pages, Jinja can
        be used in conjunction with SQL. As we
        mentioned earlier, one common usage of Jinja
        is to incorporate the backfilling of logic
        into a Hive query.

    - Add data checks early and often
        When processing data, it is useful to write
        data into a staging table, check the quality,
        and only then exchange the staging table
        with the final production table. At Airbnb,
        we call this the *stage-check-exchange*
        paradigm. Checks in this 3-step paradigm
        are important defensive mechanisms - they
        can be simple checks such as counting if
        the total number of records is greater than
        0 or something as complex as an anomaly
        detection system that checks for unseen
        categories or outliers.

    - Build useful alerts & montioring systems
        Since ETL jobs can often take a long time
        to run, it's useful to add alerts and
        monitoring to them so we do not have to
        keep an eye on the progress of the DAG
        constantly. Different companies monitor
        DAGs in many creative ways - Airbnb
        regularly uses EmailOperators to send
        alert emails for jobs missing SLAs;
        other teams have used alerts to flag
        experiment imbalances. Zymergen reports
        model performance metrics such as
        R-squared with a SlackOperator.



'''


