# dsh-lawcite-adapter — विधिक उद्धरण और दस्तावेज़ के तत्वों की जाँच

`dsh-lawcite-adapter` एक विधिक-उद्धरण सूची पढ़ता है — दस्तावेज़ का हेडर और प्रत्येक उद्धरण की एक पंक्ति — और उसी सूची की सत्यापन-योग्यता तथा दस्तावेज़-तत्वों की जाँच करता है: क्या प्रत्येक उद्धरण में विधि का नाम और अनुच्छेद संख्या लिखी है, क्या अनुच्छेद संख्या मानक चीनी रूप में है, क्या उद्धृत पाठ लिखा गया है, क्या प्रभावी-स्थिति आपकी अपनी शब्दावली से ली गई है, क्या उद्धरण में यह लिखा है कि वह कहाँ प्रयुक्त है और क्या तर्क देता है, क्या दस्तावेज़ का हेडर अपना शीर्षक और प्रकार बताता है, क्या उद्धरण संख्याएँ दोहराई नहीं गई हैं, और क्या उद्धृत पाठ के कॉलम में कोई अपूरित प्लेसहोल्डर बचा नहीं है। यह नहीं जाँचता कि कोई विधि वास्तव में मौजूद है, प्रभावी है, संशोधित या निरस्त नहीं हुई, या उस मामले पर लागू होती है।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| एक पंक्ति में अनुच्छेद संख्या दर्ज है, पर विधि का नाम खाली है। क्या यह दर्ज होता है? | हाँ। `LC-001` हर पंक्ति में विधि का नाम और अनुच्छेद संख्या (`lawName`, `articleNo`) अपेक्षित करता है और जिस पंक्ति में इनमें से एक भी न हो उसे दर्ज करता है। यह देखता है कि ये लिखे गए हैं, यह नहीं कि विधि या अनुच्छेद मौजूद है: इसमें कोई विधि-कोश नहीं है और वह उसे खोजता भी नहीं। |
| अनुच्छेद संख्या `第 577 条` लिखी है, या `第12条第3款` लिखी है। क्या यह पास हो जाएगी? | `LC-002` `articleNo` की तुलना `^第[〇零一二三四五六七八九十百千0-9]+条(之[一二三四五六七八九十]+)?$` से करता है, इसलिए स्पेस वाला रूप `第 577 条` और मिश्रित रूप `第12条第3款` दोनों दर्ज होते हैं। यह केवल संख्या का रूप देखता है, यह नहीं कि अनुच्छेद मौजूद है; अनुच्छेद का खंड या उपखंड अपने अलग कॉलम में जाता है, इसलिए `第12条` को `articleNo` में लिखें। `pattern` को अपनी संस्था की शैली के अनुसार बदला जा सकता है। |
| एक पंक्ति का उद्धृत-पाठ कॉलम खाली है और दूसरी में अब भी `【待补充】` लिखा है। क्या दोनों पकड़ में आते हैं? | हाँ, दो नियमों से। `LC-003` हर पंक्ति में `quotedText` लिखे जाने की अपेक्षा करता है; `LC-008` उस पंक्ति को दर्ज करता है जिसके `quotedText` में अब भी कोई टेम्पलेट शब्द है (`【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, `示例`)। दोनों में से कोई पाठ की तुलना विधि से नहीं करता: `LC-003` देखता है कि उद्धरण मौजूद है, `LC-008` केवल यह कि कोई प्लेसहोल्डर न बचा हो। 「略」 जानबूझकर शब्दों में नहीं है, इसलिए `……（略）` सामान्य संक्षेपण है और पास हो जाता है। |
| रिपोर्ट में `LC-004` पास होने के बजाय `skipped` दिखता है। क्यों? | क्योंकि `LC-004` की `values` सूची खाली आती है, यानी प्रभावी-स्थिति की शब्दावली कॉन्फ़िगर नहीं है, इसलिए नियम चुपचाप पास होने के बजाय स्वयं को `skipped` में दर्ज करता है। `values` में अपनी शब्दावली भरें (जैसे `现行有效`, `已修订`, `已废止`), तब `LC-004` देखता है कि `effectiveStatus` उस सूची में है या नहीं। यह सूची में होने की जाँच है, यह नहीं कि दर्ज स्थिति तथ्यों से मेल खाती है। |
| पंक्तियों में विधि का नाम और उद्धरण है, पर यह नहीं लिखा कि उद्धरण कहाँ प्रयुक्त है और क्या तर्क देता है, और हेडर में दस्तावेज़ का प्रकार भी नहीं है। क्या यह दर्ज होता है? | हाँ। `LC-005` हर उद्धरण-पंक्ति में `usage` और `purpose` अपेक्षित करता है और जिस पंक्ति में दोनों खाली हों उसे दर्ज करता है; यह नहीं आँकता कि उद्धरण वास्तव में उस तर्क का समर्थन करता है। `LC-006` हेडर में `documentTitle` और `documentType` घोषित होने की अपेक्षा करता है, और यह नहीं आँकता कि प्रकार सही चुना गया है। |
| एक ही अनुच्छेद दो अध्यायों में उद्धृत है और दोनों पंक्तियों में उद्धरण संख्या 3 है। क्या यह कोई निष्कर्ष है? | हाँ। `LC-007` सूची के भीतर दोहराई गई `citationNo` दर्ज करता है, क्योंकि दोहराई गई संख्या से फुटनोट प्रत्येक उद्धरण का पता नहीं लगा पाते। एक ही उपबंध को कई अध्यायों में उद्धृत करना सामान्य है: हर उद्धरण को अपनी संख्या दें। यह नहीं आँकता कि उसी उपबंध को दो बार उद्धृत करना उचित है या नहीं। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| 本机构法律文书审查口径（本机构配置）—— 原挂《中华人民共和国立法法》，已核实其第六十五条为立法技术条款 | 无统一标准（本条依据为本机构配置的引用管理口径）—— ⚠️ 《立法法》2023 年第二次修正文本已核实，本条不引用该法 | LC-001 |
| 本机构法律文书审查口径（本机构配置）—— 原挂《党政机关公文格式》GB/T 9704—2012，已核实为版式标准 | GB/T 9704—2012（本次未取得条文） | LC-002, LC-003, LC-005, LC-006, LC-007, LC-008 |
| 本机构法律文书审查办法（本机构配置） | 无统一标准（本条依据为本机构配置的效力口径） | LC-004 |

**Boundary:** this plugin checks a **法条引用清单** for verifiability and document elements — that each citation
names its law and article, that the article number follows the Chinese form, that a direct quotation is
transcribed, that the power status comes from your vocabulary, that the citation states where it is used and what
it argues, that the document names its title and type, that citation numbers are unique, and that no placeholder
survives. It does **not** verify that a statute exists, that it is currently in force, that it has not been amended
or repealed, or that it applies to the case.

> ### ⚠️ This plugin does not query a statute database — and that is the point
>
> **It cannot find the most consequential error: a citation to a statute or article that does not exist, or that
> has been repealed.** Confirming that requires the national laws-and-regulations database and the facts of the
> case, which is a legal professional's work. What this plugin checks is whether a citation left behind the
> elements needed to verify it — the law, the article, the quoted text, the power status, the purpose.
>
> That boundary is stated in the pack's header, in `LC-001`'s, `LC-003`'s and `LC-004`'s notes, and in the
> troubleshooting section. Read it before acting on any finding: **a clean report from this plugin is not a
> statement that the citations are correct.**
>
> `LC-002` checks the article number's *form* — `第X条` in Chinese or Arabic numerals, allowing `第X条之一` —
> and nothing about whether the article exists. `LC-003` checks that a quotation is transcribed, not that the
> transcription matches the statute. `LC-004`'s power-status vocabulary ships **empty** because no statute's
> current status is built in either.
>
> **Every `excerpt` in the rule pack says, in so many words, that the clause text was not obtained.** The regime
> lives in 《中华人民共和国立法法》, GB/T 9704—2012 and each institution's legal-document review rules. The
> verification pass could not retrieve verbatim clause text, so the pack states the gap in the `excerpt` field
> itself and keeps every rule at `warn` or `info`. **When the texts are in hand, replace each `excerpt` with the
> real clause and raise `kind` to `direct`.**
>
> ⚠️ **One basis was corrected rather than completed.** GB/T 9704—2012《党政机关公文格式》 was verified chapter by
> chapter to be a **layout** standard — paper, typesetting, binding, the placement of document elements and the
> specimen forms. **It contains no provision about citation management at all.** Six rules had been hung on it
> anyway ("every citation must name the instrument and the article", "a direct quotation must be transcribed",
> and so on). Those six now declare **the institution's own legal-document review practice** as their basis, are
> rated **`institutional-configuration`**, and therefore sit at **`info`** rather than `warn`. Leaving them at
> `warn` while their own note says "read this as the institution's practice" would have contradicted itself.
>
> **`LC-001` was then corrected the same way.** It cited 《中华人民共和国立法法》. That statute was obtained in
> full and does contain a numbering provision — 第六十五条: 「法律根据内容需要，可以分编、章、节、条、款、项、目」，with
> numbering rules and an authorisation for the NPC Standing Committee's working body to draft legislative
> technique rules. But that governs **how a law is itself drafted and numbered**; it says nothing about how an
> official document cites an existing law. So `LC-001` joins the other seven: **all eight rules in this pack now
> declare the institution's own review practice as their basis and are rated `institutional-configuration` at
> `info`.** See `rules/evidence/clause-verification-basis-mismatch.md`.

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-lawcite-adapter
dsh --profile <name> --dump-config | grep 'dsh-lawcite-adapter'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/lawcite-adapter.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-lawcite-adapter
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-lawcite-adapter contributors.
