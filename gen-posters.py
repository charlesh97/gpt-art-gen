import os
import openai
import time
import csv
import datetime 
import pickle
import requests

openai.api_key = "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"

generate_prompts = False
prompt_count = 4
art_type = "midcentury modern"
#### Generate Prompts
if generate_prompts:
  print("Generating prompts...")
  system_prompt = "You are the world's top art connoisseur with a focus on design."
  user_prompt = "Generate me {} prompts for {} artwork. In csv format separated by '|', please provide: Title, Explanation of the piece, and Description for Dalle to recreate the image with detail.".format(prompt_count, art_type)

  t_start = time.time()
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.7,
    messages=[
      {"role": "system", "content": system_prompt},
      {"role": "user", "content": user_prompt}
    ]
  )
  t_elapse = int(time.time() - t_start)
  print('***TIME ELAPSED: {}***'.format(t_elapse))
  print('***TOKEN USAGE: {}***'.format(completion.usage.total_tokens))

  ### Save object
  f = open('prompt_response.obj', 'wb')
  pickle.dump(completion, f)
  f.close()

  ### Write down log
  f = open("prompt_response.log", "w")
  f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
  f.write('\n')
  f.write(completion.choices[0].message.content)
  f.close()

else:
   f = open('prompt_response.obj','rb')
   completion = pickle.load(f)
   f.close()

### Print stats
response = completion.choices[0].message.content
print(response)

### Let's use the data ourselves (parse to CSV then put into a list)
prompt_list = list(csv.reader(response.splitlines(), delimiter='|'))
print(prompt_list)

### Roll through the list and generate folder structure for the output 
image_folder = os.getcwd() + r'/generated_images'
os.makedirs(image_folder, exist_ok=True)

for i in range(len(prompt_list)-2): #skip first two lines
  t_start = time.time()
  response = openai.Image.create(
    prompt=prompt_list[i+2][2],
    n=2,
    size="256x256"
  )
  t_elapse = int(time.time() - t_start)
  print('***TIME ELAPSED: {}***'.format(t_elapse))

  for x in range(2):
    image_url = response['data'][x]['url']
    r = requests.get(image_url)
    open(r'./generated_images/{}-{}.png'.format(i+1,x),'wb').write(r.content)

  time.sleep(25)

exit()





#---------------------------------------------------------------------------------------------------------------------

