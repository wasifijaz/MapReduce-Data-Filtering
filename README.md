## Problem Statement

Using your Hadoop distribution in DataProc (Google Cloud), solve the following task using MapReduce.

You are required to execute a MapReduce job by creating a Mapper and a Reducer. Both Mapper and Reducer need to be written in Python and executed on your terminal, including

the sorting phase. Here are the steps:

\[a\] Execute the mapper and reducer individually on NameNode (run locally).

\[b\] Share the results of mapper and reducer.

\[c\] Execute the entire setup on Hadoop using streaming service

\[d\] Share the results and screenshot

## Task

**Implement one executable MapReduce job that receives as input two .csv tables having the structure: - Table A: StudentId, Name, DOB - Table B: StudentId, CourseId, Grade The Map Reduce job needs to perform the following SQL query:**

**select StudentId, Name, CourseId, Grade**

**from A**

**join B on A.StudentId = B.StudentId**

**where DOB >= 1995-01-01**

**Therefore, if the two original tables are:**

| StudentId | Name | DOB |
| --- | --- | --- |
| M575757 | Alice | 1994-01-05 |
| --- | --- | --- |
| M212121 | Tom | 1993-02-07 |
| --- | --- | --- |
| M989898 | John | 1995-06-02 |
| --- | --- | --- |

| StudentId | CourseId | Grade |
| --- | --- | --- |
| M575757 | CSD1414 | pass |
| --- | --- | --- |
| M575757 | CSD5050 | distinction |
| --- | --- | --- |
| M575757 | CSD5566 | merit |
| --- | --- | --- |
| M212121 | CSD1414 | distinction |
| --- | --- | --- |
| M212121 | CSD5050 | distinction |
| --- | --- | --- |
| M212121 | CSD5566 | distinction |
| --- | --- | --- |
| M989898 | CSD5050 | merit |
| --- | --- | --- |
| M989898 | CSD5566 | distinction |
| --- | --- | --- |

**The final table should be:**

| StudentId | Name | CourseId | Grade |
| --- | --- | --- | --- |
| M575757 | John | CSD5050 | merit |
| --- | --- | --- | --- |
| M575757 | John | CSD5566 | distinction |
| --- | --- | --- | --- |

## Solution

### GCP Cluster

#### Creation of GCP Cluster

Find Dataproc in the GCP console, create a cluster using the compute engine. Give a name to the cluster.

1. Select OS, for my cluster I have chosen Ubuntu 22 with Hadoop 3.3 and Spark 3.3.
2. Enable component gateway.
3. Configure Manager and Worker Node.

### Mapper

### Method Overview

The wasif_mapper.py script is designed to prepare data for processing in a MapReduce environment, simulating the "Map" phase. It processes two types of input data: student information and grades, by reading from CSV files. The script performs the following steps:

1. **Reading CSV Files:** The read_csv function reads a CSV file and returns a list of dictionaries. Each dictionary maps a student ID to relevant details (grades and student information).
2. **Mapping Functions:**
    1. **map_grades(parts):** Extracts and returns a dictionary with the student ID as the key and a list containing the course ID and grade as values.
    2. **map_students(parts):** Extracts and returns a dictionary with the student ID as the key and a list containing the student name and date of birth (DOB) as values.
3. **Data Combination:**
    1. After reading and mapping the data from both files, the script creates a dictionary (student_dict) from the list of student information.
    2. It then iterates through each entry in the grades list, combining it with corresponding student details from student_dict. The combined entry contains the student ID, name, DOB, course ID, and grade.
    3. These combined entries are then printed, making them available for the next phase of processing (Reduce).

#### How the Mapper Script Works

1. The script starts by checking if the correct number of arguments (file paths for grades and students) are provided.
2. It reads and processes each CSV file using the read_csv function.
3. The resulting data structures from each file are then combined based on student IDs.
4. The combined list of student details and grades are printed to stdout, formatted to be consumed by the reducer script.

### Mapper Output Local

#### Local System Execution Steps & Commands

1. **_source venv/bin/activate_** (To activate python environment)
2. **_cd ADA\\ Mini\\ Block\\ 4\\ -\\ \\ Wasif\\ Ijaz/_** (To navigate the folder)
3. **_python wasif_mapper.py grades.csv students.csv_** (To run mapper code)

#### GCP Master Node Local Execution Steps & Commands

1. **_Upload file in GCP Environment_**
2. **_python wasif_mapper.py grades.csv students.csv_** (To run mapper code)

#### Beautified Local Mapper Output

\[

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_1414_'_, _'pass'_ \]

},

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_5050_'_, _'distinction'_ \]

},

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_5566_'_, _'merit'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_1414_'_, _'distinction'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_5050_'_, _'distinction'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_5566_'_, _'distinction'_ \]

},

{

_'M989898'_: \[ _'John'_, _'_1995-06-02_'_, _'CSD_5050_'_, _'merit'_ \]

},

{

_'M989898'_: \[ _'John'_, _'_1995-06-02_'_, _'CSD_5566_'_, _'distinction'_ \]

}

\]

### Mapper Output Hadoop (GCP Cluster)

#### Steps & Commands

1. **_Upload files to Hadoop Environment_**
2. **_hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \\_**

**_\-D mapreduce.job.reduces=1 \\_**

**_\-D mapreduce.input.fileinputformat.split.maxsize=134217728 \\_**

**_\-D mapreduce.input.fileinputformat.split.minsize=134217728 \\_**

**_\-files hdfs:///user/wasif_studentmdx/scripts/wasif_mapper.py,hdfs:///user/wasif_studentmdx/data/grades.csv,hdfs:///user/wasif_studentmdx/data/students.csv \\_**

**_\-mapper "python3 wasif_mapper.py grades.csv students.csv" \\_**

**_\-input hdfs:///user/wasif_studentmdx/data/data \\_**

**_\-output /user/wasif_studentmdx/outputMapper_**

1. **_hdfs dfs -cat /user/wasif_studentmdx/outputMapper/part-\*_** (To view output)

#### Beautified GCP Cluster Mapper Output

\[

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_1414_'_, _'pass'_ \]

},

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_5050_'_, _'distinction'_ \]

},

{

_'M575757'_: \[ _'Alice'_, _'_1994-01-05_'_, _'CSD_5566_'_, _'merit'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_1414_'_, _'distinction'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_5050_'_, _'distinction'_ \]

},

{

_'M212121'_: \[ _'Tom'_, _'_1993-02-07_'_, _'CSD_5566_'_, _'distinction'_ \]

},

{

_'M989898'_: \[ _'John'_, _'_1995-06-02_'_, _'CSD_5050_'_, _'merit'_ \]

},

{

_'M989898'_: \[ _'John'_, _'_1995-06-02_'_, _'CSD_5566_'_, _'distinction'_ \]

}

\]

### Reducer

### Method Overview

The wasif_reducer.py script is designed to simulate the "Reduce" phase in a MapReduce environment. It processes the output from the mapper script to perform filtering and aggregation tasks. Here's what it does:

1. **Reading Input:** It reads from standard input (sys.stdin), where each line represents a dictionary containing a student ID and their corresponding details (including grades).
2. **Processing and Filtering:**
    1. The script iterates over each input line, evaluates it (converts string to dictionary), and processes the data.
    2. It checks if the current student ID is different from the last processed one. If true, it processes and prints the previous student's data (if they meet the DOB condition).
    3. The script accumulates course and grade information for each student.
3. **Final Output:**
    1. After iterating through all data, the script checks the last student's information and prints it if they meet the condition (DOB ≥ 1995-01-01).
    2. The output is formatted as "StudentId, Name, CourseId, Grade", mimicking the structure of an SQL SELECT statement.

#### How the Reducer Script Works

1. Processes one line at a time from the mapper's output.
2. Maintains a current student context and accumulates course grades.
3. Filters out students based on their DOB and prints details for students born on or after January 1, 1995.


### Reducer Output Local

#### Local System Execution Steps & Commands

1. **_source venv/bin/activate_** (To activate python environment)
2. **_cd ADA\\ Mini\\ Block\\ 4\\ -\\ \\ Wasif\\ Ijaz/_** (To navigate the folder)
3. **_python wasif_mapper.py grades.csv students.csv | sort | python wasif_reducer.py_** (To run reducer code)

#### GCP Master Node Local Execution Steps & Commands

1. **_Upload file in GCP Environment_**
2. **_python wasif_mapper.py grades.csv students.csv | sort | python wasif_reducer.py_** (To run reducer code)

#### Beautified Local Reducer Output

| StudentId | Name | CourseId | Grade |
| --- | --- | --- | --- |
| M575757 | John | CSD5050 | merit |
| --- | --- | --- | --- |
| M575757 | John | CSD5566 | distinction |
| --- | --- | --- | --- |

###

### Reducer Output Hadoop (GCP Cluster)

#### Steps & Commands

1. **Upload files to Hadoop Environment**
2. **hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \\**

**\-D mapreduce.job.reduces=1 \\**

**\-D mapreduce.input.fileinputformat.split.maxsize=134217728 \\**

**\-D mapreduce.input.fileinputformat.split.minsize=134217728 \\**

**\-files hdfs:///user/wasif_studentmdx/scripts/wasif_mapper.py,hdfs:///user/wasif_studentmdx/scripts/wasif_reducer.py,hdfs:///user/wasif_studentmdx/data/grades.csv,hdfs:///user/wasif_studentmdx/data/students.csv \\**

**\-mapper "python3 wasif_mapper.py grades.csv students.csv" \\**

**\-reducer "python3 wasif_reducer.py" \\**

**\-input hdfs:///user/wasif_studentmdx/data/**

1. **hdfs dfs -cat /user/wasif_studentmdx/output/part-\***

####

#### Beautified GCP Cluster Reducer Output

| StudentId | Name | CourseId | Grade |
| --- | --- | --- | --- |
| M575757 | John | CSD5050 | merit |
| --- | --- | --- | --- |
| M575757 | John | CSD5566 | distinctionLocal |
| --- | --- | --- | --- |

###

#### Job Execution Details

- **_Job ID:_** job_1712956789496_0039 was the identifier for the Hadoop job, used for tracking and managing the job within the Hadoop ecosystem.
- **_Execution Time:_** The job counters indicate that the total time taken by all map tasks was 194,0957 milliseconds (approx. 19.41 seconds), and the total time taken by all the reduce tasks was 516,1957 milliseconds (approx. 5.16 seconds). This shows the efficiency of the job execution in terms of processing time.

#### Map-Reduce Framework

- The counters show that there was a total of 1 map task and 1 reduce task launched for the job.
- The number of processed map output records was 3, indicating that 3 key-value pairs were emitted by the mapper.
- However, the reduce output records were 2, suggesting that the reducer has processed and emitted 2 key-value pairs as output.

#### File System Counters

- A total of 499 bytes of data were read and 489 bytes of data were written by the Hadoop job.This is due to a very small dataset.

### Complete Commands and Explanation

1. **python wasif_mapper.py grades.csv students.csv**

_(Run Python script wasif_mapper.py with input files grades.csv and students.csv.)_

1. **python wasif_mapper.py grades.csv students.csv | sort | python wasif_reducer.py**

_(Pipe the output of the first command to sort, then to wasif_reducer.py.)_

1. **hdfs dfs -mkdir /user/wasif_studentmdx**

_(Create a directory named wasif_studentmdx in HDFS.)_

1. **hdfs dfs -mkdir /user/wasif_studentmdx/scripts**

_(Create subdirectory scripts within wasif_studentmdx.)_

1. **hdfs dfs -mkdir /user/wasif_studentmdx/data**

_(Create subdirectory data within wasif_studentmdx.)_

1. **hdfs dfs -put grades.csv /user/wasif_studentmdx/data**

_(Upload grades.csv to HDFS under wasif_studentmdx/data.)_

1. **hdfs dfs -put students.csv /user/wasif_studentmdx/data**

_(Upload students.csv to HDFS under wasif_studentmdx/data.)_

1. **hdfs dfs -ls /user/wasif_studentmdx/data**

_(List files in the data directory of wasif_studentmdx.)_

1. **hdfs dfs -put wasif_mapper.py /user/wasif_studentmdx/scripts**

_(Upload wasif_mapper.py to HDFS under wasif_studentmdx/scripts.)_

1. **hdfs dfs -put wasif_reducer.py /user/wasif_studentmdx/scripts**

_(Upload wasif_reducer.py to HDFS under wasif_studentmdx/scripts.)_

1. **hdfs dfs -ls /user/wasif_studentmdx/scripts**

(_List files in the scripts directory of wasif_studentmdx.)_

1. **hdfs dfs -chmod +x /user/wasif_studentmdx/scripts/wasif_mapper.py**

_(Change the permissions of wasif_mapper.py in HDFS to be executable.)_

1. **hdfs dfs -chmod +x /user/wasif_studentmdx/scripts/wasif_reducer.py**

_(Change the permissions of wasif_reducer.py in HDFS to be executable.)_

1. **hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \\**

**\-D mapreduce.job.reduces=1 \\**

**\-D mapreduce.input.fileinputformat.split.maxsize=134217728 \\**

**\-D mapreduce.input.fileinputformat.split.minsize=134217728 \\**

**\-files hdfs:///user/wasif_studentmdx/scripts/wasif_mapper.py,hdfs:///user/wasif_studentmdx/data/grades.csv,hdfs:///user/wasif_studentmdx/data/students.csv \\**

**\-mapper "python3 wasif_mapper.py grades.csv students.csv" \\**

**\-input hdfs:///user/wasif_studentmdx/data/data \\**

**\-output /user/wasif_studentmdx/outputMapper**

_(Run a Hadoop streaming job with specified configurations and files, using wasif_mapper.py as the mapper function.)_

1. **hdfs dfs -cat /user/wasif_studentmdx/outputMapper/part-\***

_(Display the contents of the output files generated by the mapper job.)_

1. **hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \\**

**\-D mapreduce.job.reduces=1 \\**

**\-D mapreduce.input.fileinputformat.split.maxsize=134217728 \\**

**\-D mapreduce.input.fileinputformat.split.minsize=134217728 \\**

**\-files hdfs:///user/wasif_studentmdx/scripts/wasif_mapper.py,hdfs:///user/wasif_studentmdx/scripts/wasif_reducer.py,hdfs:///user/wasif_studentmdx/data/grades.csv,hdfs:///user/wasif_studentmdx/data/students.csv \\**

**\-mapper "python3 wasif_mapper.py grades.csv students.csv" \\**

**\-reducer "python3 wasif_reducer.py" \\-input hdfs:///user/wasif_studentmdx/data/data \\**

**\-output /user/wasif_studentmdx/output**

_(Run another Hadoop streaming job with specified configurations and files, using both mapper and reducer scripts.)_

1. **hdfs dfs -cat /user/wasif_studentmdx/output/part-\*hdfs dfs -cat /user/wasif_studentmdx/output/part-\***

_(Display the contents of the output files generated by the mapper and reducer job. Display the contents of the output files generated by the final job)_

### Conclusion

The combined use of wasif_mapper.py and wasif_reducer.py effectively performs a SQL-like JOIN operation on two datasets (students and grades) and then filters the results based on a condition (DOB ≥ 1995-01-01). This approach leverages the MapReduce programming model, which is suitable for processing large datasets distributed across multiple nodes in a cluster. The mapper script prepares and combines the data, while the reducer script performs the final filtering and output formatting. This method is highly scalable and efficient for large-scale data processing tasks.

The Hadoop streaming job was successfully executed with a single mapper and reducer. The mapper generated three key-value pairs, the reducer completed the task with two output records. The reducer was designed to operate on input from the mapper, or that the mapper's job was to merely pass the data to the reducer in an joined form. Filtration is performed in the reducer. Below graphs provide insights into resource utilization and can help diagnose performance bottlenecks or inefficiencies in my MapReduce jobs.

#### Resource Utilization Graphs

Disk Operations Graph: This graph represents the disk operations over time on my GCP cluster nodes during the execution of my MapReduce jobs. The spikes indicate moments when my jobs are reading from or writing to the disk. A particularly high peak suggest a shuffle operation, where data is exchanged between nodes, or a checkpointing activity where intermediate data is saved to disk.

Disk Bytes Graph: This one is similar to the disk operations graph but focuses on the amount of data read from or written to the disk. The peaks suggest intensive disk I/O activities, which can occur during data-intensive stages of my jobs, like loading large datasets or writing out results.

Network Packets Graph: This graph displays the network packets sent and received over time. Peaks in this graph align with the shuffle and sort phases of my MapReduce processes, where there's a network-intensive exchange of data between different nodes.

Network Bytes Graph: This shows the volume of data transmitted over the network. High values can indicate data transfer between nodes, possibly during the shuffle phase of MapReduce, which is bandwidth-intensive.

CPU Utilization Graph: The CPU utilization graph indicates the processing power used by my cluster over time. Spikes are associated with computationally heavy operations such as map or reduce tasks or complex data transformations.

YARN Memory Graph: This graph represents the memory usage managed by YARN (Yet Another Resource Negotiator), which handles resource allocation for the jobs. Sharp increases point to memory-intensive operations or a possible memory leak if the memory is not released after job completion.

### References

The Mapper and Reducer code were developed based on custom logic (written by myself) inspired by foundational principles outlined in the foundational resources including "ChatGPT" \[1\] and a tutorial on MapReduce from the High-Performance Data Analytics course \[2\]. These resources were only used for basic understanding and challenge has been done myself including writing code of Mapper and Reducer.

\[1\] OpenAI. "ChatGPT." Retrieved from <https://chat.openai.com/>

\[2\] High-Performance Data Analytics Course. (2022). "Exercise 04: Introduction to MapReduce." Retrieved from <https://hps.vi4io.org/_media/teaching/autumn_term_2022/hpda22-exercise-04.pdf>