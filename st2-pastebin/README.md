# Pastebin pack for stackstorm

**Polling Sensor pastebin.PasteBinPoller**

* Routinely polls the [Pastebin scraping API endpoint](https://pastebin.com/doc_scraping_api) looking for new uploads.
* It uses the kv store to keep a record of the most recently handled paste so you don't keep hitting old ones
* Emits `pastebin.new_paste`
    * Payload is nearly every field listed on the above URL, the main ones you'll use are:
    * `key` is the 8 character string which refers to individual pastes
    * `date` is a seconds-since-unix-epoch-time timestamp of the paste
    * `title` of the paste
    * `syntax`
    * `size` of the paste
    * `user` who pasted it

**Action pastebin.scrape_paste_raw**

Give it the `key` and it'll grab the raw text of the paste

**Action pastebin.scrape_paste_metadata**

Give it the `key` and it'll grab the metadata of the paste

## Usage

1. [Get a pastebin pro account](https://pastebin.com/pro) and whitelist your IP address [on the scraping API page](https://pastebin.com/doc_scraping_api).
2. Install the pack: `st2 pack install https://bitbucket.org/yaleman/st2-pastebin`
3. Set the configuration items:
    * If your source IP is IPv4 or IPv6, set the `ipversion` value to the integer 4 or 6. This works around the fact that Pastebin is available on dual stack, but you can only whitelist one IP.
    * `poll_maxresults` can limit incoming bandwidth by requesting less items.
    * `poll_interval` is the number of seconds between polls - this will update every poll cycle if you change it
4. Configure a rule that uses the sensor/actions

## Example rule

Trigger type: patebin.new_paste
Action ref: pastebin.scrape_paste_raw
Action key: {{trigger.key}} 

This'll grab every new paste and then the contents of it. It's a super simple example which shouldn't be used alone, but could be used for an [ActionChain](https://docs.stackstorm.com/actionchain.html) workflow to filter contents and generate alerts.