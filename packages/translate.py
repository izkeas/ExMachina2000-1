import requests
import sys

def splitRegion(lang):
  regional_variant = ""

  if lang.__contains__("-"):
    split = lang.split("-")
    regional_variant = split[1]
    lang = split[0]

  return lang, regional_variant

def translate(src, tar, content) -> str:
  source_lang, s_regional_variant = splitRegion(src)
  target_lang, t_regional_variant = splitRegion(tar)

  data={
      "jsonrpc": "2.0",
      "method": "LMT_handle_jobs",
      "params": {
        "commonJobParams":{
          "formality": None
        },
        "jobs": [
          {
            "kind": "default",
            "preferred_num_beams": 4,
            "quality": "fast",
            "raw_en_context_before": [],
            "raw_en_context_after": [],
            f"raw_en_sentence": content
          }
        ],
        "lang": {
          "user_preferred_langs": [
            "PT",
            "EN"
          ],
          "source_lang_user_selected": source_lang,
          "target_lang": target_lang
        },
        "timestamp": 1613684719050
      }
    }

  if s_regional_variant :
    data["params"]["commonJobParams"]["regionalVariant"] = f"{source_lang.lower()}-{s_regional_variant}"

  if t_regional_variant :
    data["params"]["commonJobParams"]["regionalVariant"] = f"{target_lang.lower()}-{t_regional_variant}"
  
  res = requests.post("https://www2.deepl.com/jsonrpc", json=data).json()
  try:
    results = res["result"]["translations"][0]["beams"]
    return [x["postprocessed_sentence"] for x in results]
  except:
    if (res["error"]["message"]):
      return [f"Error: "+res["error"]["message"]]