# r.AID.ologist 🖊️
### 🔍**Description of the system**
r.AID.ologist is a framework designed for radiologists to provide assistance on the generation of medical reports. 
It is devised as a Case-Based Reasoning model, powered by several deep learning models which have been included to improve its performance, as well as providing additional features.  

While CBR is integrated as a continuous cycle, its subparts are designed to be fully modular, thus can be easily substituted to fit new data. The following diagram provides an overview on the system. Modular elements are represented by bricks, implying that they can be replaced by different models as long as they meet the same objective. 

<img src="https://i.ibb.co/7Y4ZyhR/Global-Diagram.png" width=50% height=50%>

### 🧱**Module specification**
The implementations of the different modules are contained in the *functions.py* file from the internal_functions folder. By default, the following models are employed for each of the denoted modules:
#### Retrieve Modules
 1. ***Image feature extraction***: A combination of a keypoint-based image feature algorithm (KAZE) and a pretrained Convolutional Neural Network (ResNet18). 
 2. ***Document embedding***:  An English pretrained model from SciSpacy is used (en_core_sci_md)
 3. ***Named Entity Recognition***: An external resource, CliNER, is employed for this task. The employed pretrained model works for English textual data, and distinguishes between three types of named entities: problems, treatments and tests. These types **MUST** remain unchangeable in case of substitution. 
 4. ***Noise filtering***: SciSpacy is used to detect existing abbreviations. The ratio of identified abbreviations is obtained as *#_(detected_abbreviations ^ existing_tokens)/ #_detected abbreviations*

#### Reuse Modules
 1. ***Sectioning Model***: A bidirectional LSTM, implemented via Pytorch, is used to section the input report. The employed sectioning model, alongside its functions, is implemented in the *section_model.py* file contained in the internal_functions folder. In this default model, four sections are considered: **Findings, Comparison, Indication and Impression**
 2. ***Scoring Model***: A combination of the aforementioned SciSpacy embedding model with a Random Forest Classifier is employed  to score each report as valid (1) or rejected (0).
 3. ***Abbreviation Disambiguation***: The aforementioned SciSpacy English pretrained model is used to extract existing abbreviations. SNOMED's query service is then used to obtain potential disambiguations for each of the detected abbreviations.

### 🖱️ **Installation**
A ready-to-use version of the framework is available as a Docker image in **elviish/raidologist:latest**. Once downloaded, the image can be ran with the command:

    docker run --name raidologist -p *selected_port*:5000 elviish/raidologist:latest
  
The framework has been developed using Python 3.7. To locally run the framework,  or o modify it, these are the steps to follow:

 1. Clone the repository
 `git clone https://github.com/oeg-upm/AI4EU_raidologist.git`
 
 2. Install the required dependencies
 `pip install -r requirements.txt`
 
 3. Install the spacy model
 `python -m spacy download en_core_web_sm`
 
 4. Download the NER model and place it the directory *externals/i2b2*
`curl -O https://drive.upm.es/s/gOXyNxXgnrDBIEj/download`

 5. Execute the *main.py* file 
`python main.py`

 6. Go to the direction localhost:5000 in your web browser to start using the framework

Issues can be reported at https://github.com/oeg-upm/AI4EU_raidologist/issues

### ❓ **About**
This framework has been developed as part of the AI4EU project. 

It is licensed under APACHE 2.0.

   
    


 


