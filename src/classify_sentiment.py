import pickle
import nltk
import os
import json
import re
from google.cloud import translate


def csvToDict():


  sentence_list = {}
  translate_client = translate.Client()
  hangul = re.compile('[^ ㄱ-ㅣ가-힣A-Za-z?!]+')

  idx = 0
  with open('comment.csv', 'r', encoding='utf-8') as cs :
    rf = csv.reader(cs, delimiter=',')
    for row in rf:

      comment = row[1].replace('\ufeff', '')
      removed_emoji = hangul.sub('', comment)
      if len(removed_emoji) > 3:
          translation = translate_client.translate(removed_emoji, target_language='ko')
          translated_sentence = translation['translatedText']

          predict = labels2names[net.predict_from_sentence(translated_sentence.split(), text2features)]
          sentence_list[idx] = {'sentence': comment, 'label': predict}
          idx += 1

  print(sentence_list)
  return sentence_list


def dictTojson(sentence_dict):

  with open('classfiedComment.json', 'w', encoding='utf-8') as file :
        json.dump(sentence_dict, file, ensure_ascii=False, indent='\t')


​
def explicit():
    from google.cloud import storage
​
    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'My First Project-bd5a02e9b8ce.json')
​
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


def test_explicit():
    with open(os.environ['GOOGLE_APPLICATION_CREDENTIALS']) as creds_file:
        creds_file_data = creds_file.read()
​
    open_mock = mock.mock_open(read_data=creds_file_data)
​
    with mock.patch('io.open', open_mock):
        explicit()
​

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="My First Project-bd5a02e9b8ce.json"
test_explicit()

print(translation['translatedText'])
​
nltk.download('wordnet')
nltk.download('stopwords')
filename = "dataset/test_dataset_bow.pkl"
with open(filename, "rb") as fp:
  X_test, Y_test, labels2names, text2features = pickle.load(fp)


filename = "trained_model_gboost.pkl"
with open(filename, "rb") as fp:
    net = pickle.load(fp)

sl = csvToDict() # sentence dictionary
dictTojson(sl)
