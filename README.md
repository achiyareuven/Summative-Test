"# Summative-Test" 


# "program flow"

## "I divided the program into four servers"

### Each service is in a separate folder and each has a manager with which the service is run.

**First service preprocessing** Extracts metadata on audio files 
Sends a message in Kafka with metadata on each file including path"

**A second service save data** reads the message, adds a unique identifier from 
the elastic index to the metadata, and writes the file itself to MongoDB with the same unique identifier and sends a message in Kafka the metadata with the unique identifier.

**Third service STT** reads the messages from the previous service reads the file from Mongo by id 
converts the audio to text updates the text field in Elasticsearch 
and sends a new message in Kafka to the next service

**The fourth service enrich**, reads the messages from the previous service, processes the text, and adds fields to Elastic.

# Significant decisions I made

### In the second part in the save_data folder

In the consumer I passed the commit to the manager who will commit only after it has managed to save to Mongo and Elastic

And I built the unique identifier from a combination of size and path so that it is unique

### In the third part in the convet_to_text folder

I decided to split it into another service that wouldn't get stuck because the conversion takes time

In the consumer I set a large max_poll_interval_ms so that it wouldn't be thrown out of the group in the middle of processing

I did the transcription with speech_recognition and not with others so as not to download a model and have problems with the dacker

I read the file from Mongo into a temporary file and deleted it later so that I wouldn't have any leftovers



### In the fourth part in the enrich folder

I chose the logic to calculate the risk percentage by the dangerousness score divided by the dangerousness maximization. I calculated two points for each word, considering that even the most dangerous text always has neutral words.

I added stop word deletion using nltk to avoid calculating irrelevant words.

I used base64 to decode the encoding.



# Code explanation



## first service data_preparation

**Divided into three files** The first file initial_processing
Receives an audio file Extracts metadata Returns a dictionary with the file's metadata

**The second file kafka_producer** sends the metadata of each file as a message in Kafka with a topic.

**The second file kafka_producer** sends the metadata of each file as a message in Kafka with a topic.




