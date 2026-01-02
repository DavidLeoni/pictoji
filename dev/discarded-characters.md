# Discarded characters

**Unicode issues:**

🫵 🫳 🫱 are from Emoji 14.0, released September 2021 with Unicode 14.0. Microsoft only ships full Emoji 14.0
Windows 10's emoji font, Segoe UI Emoji, hasn't been updated to include them. 
+ support [in Windows 11](https://learn.microsoft.com/en-us/typography/fonts/windows_11_font_list)

|Minimum Version |    Unicode Level   |
|----------------|--------------------|
|1903+ (May 2019)|     Unicode 12.0   |
|21H2+ (Nov 2021)|     Unicode 13.0   |
| Any version    | Never Unicode 14.0+|


🞉: looks like just a bold O?
❍: too confusing
◉, ◎: may look like a radio button
ꕕ:Vai: can be confused with ⨂:math_supp_ops 
⊗:math_ops: can be confused with ⨂:math_supp_ops  
⊗︎:math_ops + U+FE0E VARIATION SELECTOR-15 for emoji display, ignored by most renderers:
   can be confused with ⨂:math_supp_ops  
⊗⃝: U+2297 + U+20DD: composite, avoid, use this instead ⨷
田:CJK_Unified_Ideograph too similar to ⊞:math_op
➰: emoji, bad contrast

∴: has already math meaning 'therefore', only found in old math papers
ට: looks too much like derivative
၉: too similar to ဨ  
⧟:math: too close to ⚯
ン: almost identical to ソ
ニ:Katakana modern japanese, too similar to ㆓:Kanbun historical chinese/japanese
二:CJK_Unified_Ideographs: , too similar to ㆓:Kanbun historical chinese/japanese
㆔:Kanbun historical chinese/japanese, too similar to 𝛯:math 
Ξ:Greek_capital_Xi, too similar to 𝛯:math
𝝣:Math_bold_capital_Xi, too similar to 𝛯:math
ሪ: may look like a 6 
∩: confused with ⋂
∪: confused with ⋃
℘: even if it is the official power set unicode symbol, prefer 2^S as ℘ is visually convoluted, we need to define 2^S meaning anyway, we already have too many Ps, we don't want too expose powerset to users too much as it's a difficult concept more for theory


### Discarded boxes (all to similar to ▢ : empty relation U+25A2 WHITE SQUARE WITH ROUNDED CORNERS)
☐ U+2610 Miscellaneous Symbols — Ballot Box
□ : U+25A1, Geometric Shapes — White Square
🗆 : U+1F5C6, empty note 
🗌 : U+1F5CC 
◻ : U+25FB, Geometric Shapes — White Medium Square (legacy)  
⬜ : U+2B1C, Miscellaneous Symbols and Arrows — White Large Square  
▫ : U+25AB, Geometric Shapes — White Small Square  
◽ : U+25FD, Geometric Shapes — White Medium Small Square  
▯ : U+25AF, Geometric Shapes — White Vertical Rectangle  
❏ : U+274F, Dingbats — Square With Contoured Outline  
❐ : U+2750, Dingbats — White Square Containing Black Small Square  
❑ : U+2751, Dingbats — Ballot Box With Light X  
❒ : U+2752, Dingbats — Ballot Box With Bold Check  
⧠ : U+29E0, Miscellaneous Mathematical Symbols-B — Square Containing Black Small Square  
⎕ : U+2395, Misc Technical — APL Functional Symbol Quad  
⌷ : U+2337, Misc Technical — Left Square Bracket With Quill  
ロ : U+30ED, Katakana Letter RO (Japanese syllable, not a symbol)  

㊁:Enclosed CJK(two): too similar to ㋥:Katakana

Question marks - very useful but often unstable:

⍰ : used as tofu on some systems
⯑ : Added in Unicode 10.0 (2017), still risky on older Android devices.[1] It renders as a monochrome text glyph on most systems.
🯄 : too new: added in Unicode 13.0 (2020) under the "Symbols for Legacy Computing" block. Mobile Support is Poor: Windows 10/11, macOS render well (using Segoe UI Symbol or Apple Symbols), but iOS and Android default fonts often lack glyphs for this specific block.



Too similar to ▇ : universal relation  U+2587 UPPER SEVEN EIGHTHS BLOCK

■ : U+25A0 BLACK SQUARE 
◼ : U+25FC BLACK MEDIUM SQUARE  
⬛ : U+2B1B LARGE BLACK SQUARE
▉ : U+2589 LEFT SEVEN EIGHTHS BLOCK


Ꙩ:CyrillicExtB: too similar to ☉
ꖴ:Vai: too similar to ☉
Ꙫ:CyrillicExtB: too similar to ⚇


⨉: N-ARY TIMES OPERATOR, U+2A09
×: multiplication sign, Latin-1 Supplement U+00D7
✕: MULTIPLICATION, Dingbats, U+2715
✖❗❗ :	Heavy multiplication X, Dingbats, U+2716 can show emoji black even with black backround
⤫: Rising diagonal crossing falling diagonal, Supplemental Arrows-B, 0x292b
⤬ Falling diagonal crossing rising diagonal, Supplemental Arrows-B,  0x292c
╳: LIGHT DIAGONAL CROSS, Box Drawing, U+2573
🝍❗ 
🞨❗:	THIN SALTIRE, Geometric Shapes Extended, U+1F7A8
🞩❗:	LIGHT SALTIRE, Geometric Shapes Extended, U+1F7A9
🞪❗:	MEDIUM SALTIRE, Geometric Shapes Extended, U+1F7AA
🞫❗:	BOLD SALTIRE, Geometric Shapes Extended, U+1F7AB
🞬❗❗ : HEAVY SALTIRE, Geometric Shapes Extended, U+1F7AC interesting but poor render support  
🞭❗:	VERY HEAVY SALTIRE, Geometric Shapes Extended, U+1F7AD
🞮❗:	EXTREMELY HEAVY SALTIRE, Geometric Shapes Extended, U+1F7AE
🗙❗:	CANCELLATION X, U+1F5D9



## Langs review

- Imperial Aramaic: no, Right to left

- Malayalam: ഺ❗ ൜❗

- Telugu: ౸❗ ౺❗ ౻❗ ౽❗ ౾❗ ౿❗ ౡ❗ ౷❗:Telugu

- Kannada: ಀ❗ ೞ❗

- Sinhala:   ෴❗ ෧❗ ෨❗ ෩❗ ෯❗
- Sinhala Archaic Numbers:  𑇡❗ 𑇢❗ 𑇣❗ 𑇥❗

- Ahom: 𑜽❗ 𑜾❗ 𑜙❗ 𑜕❗ 𑜖❗ 𑜍❗

- Balinese: ᬉ❗ ᭨❗ ᭢❗ ᭣❗ ᭤❗ ᭥❗ ᭕❗ ᬧ❗ ᭞❗ 	

- Batak: 	ᯣ❗ ᯋ❗ ᯡ❗ ᯙ❗ ᯅ❗ ᯤ❗ ᯥ❗ ᯼❗ ᯽❗

- Bhaiksuki : 𑰪❗ 𑰤❗ 𑰆❗ 𑰧❗ 𑰇❗ 𑱢❗  

- Buhid: ᝀ❗ ᝁ❗ ᝂ❗ ᝃ❗ ᝄ❗ ᝅ❗ ᝆ❗ ᝉ❗ ᝊ❗ ᝌ❗ ᝏ❗ ᝐ❗

- Buginese: ᨖ❗ ᨁ❗ ᨄ❗ ᨉ❗ ᨊ❗ ᨌ❗ ᨎ❗ ᨑ❗ ᨏ❗ ᨟❗

- Chakma: 𑄕❗ 𑄦❗ 𑅀❗ 𑄷❗

- Cham: ꩑❗ ꨂ❗ ꩜❗ ꩟❗ ꨝ❗ 

Common Indic Number Forms: 

- Dogra: 𑠕❗

- Grantha: 𑌲❗ 𑍞❗ 𑍟❗

- Hanunoo: ᜠ❗ ᜧ❗ ᜢ❗ ᜣ❗

- Javanese: ꧁❗ ꧂❗ ꧙❗ ꧞❗ ꦎ❗

- Kaithi: 𑂝❗ 𑂞❗ 𑂉❗

- Khmer: 

- Khojki: 𑈥❗ 𑈸❗ 𑈹❗ 𑈼❗ 𑈣❗ 𑈞❗ 𑈃❗

- Khudawadi: 𑋄❗ 𑋜❗ 𑋷❗ 𑋱❗ 𑋕❗ 𑊾❗ 𑊳❗

- Lao:  

- Lepcha: ᰓ❗ ᰗ❗ ᰝ❗ ᰟ❗ ᰢ❗ ᰾❗ ᰜ❗ ᰒ❗ ᰇ❗

- Limbu: ᤀ❗ ᥋❗ ᤛ❗ ᤔ❗	

- Mahajani: 𑅐❗ 𑅗❗ 

- Meetei Mayek:    

- Meetei Mayek Extensions: ꫤ❗ ꫥ❗ ꫦ❗ ꫧ❗ ꫪ❗ ꫳ❗ ꫱❗ 	    

- Modi: 𑘪❗

- Multani: 𑊢❗ 𑊓❗ 𑊂❗

- Myanmar: ၓ❗ ၕ❗ ၦ❗ ၡ❗ ၵ❗ ၻ❗ ၼ❗

- Myanmar Extended-A: ꩺ❗ ꩦ:❗ ꩦ❗:variation ꩧ❗ ꩰ❗ ꩳ❗   


- Myanmar Extended-B:  ꧩ❗ ꧪ❗ ꧫ❗ ꧬ❗ ꧭ❗ ꧺ❗ ꧻ❗ ꧼ❗ ꧽ❗

- New Tai Lue: ᦹ❗ ᦙ❗ ᦥ❗ ᦰ❗ ᦉ❗ ᦈ❗ 

- Newa: 𑐛❗ 𑑛❗ 𑑗❗ 𑑝❗

- Phags-pa (warning: vt/hz): ꡪ❗ ꡴❗ ꡟ❗ ꡇ❗ ꡅ❗ ꡣ❗   

- Rejang: ꤱ❗ ꥁ❗ ꤸ❗ ꥟❗ ꤹ❗ ꤼ❗ ꤰ❗ 

- Saurashtra: ꢂ❗ ꢞ❗ ꢔ❗ ꢮ❗ ꢳ❗ ꣗❗ ꣘❗ ꣕❗	

- Sharada: 𑆗❗ 𑆣❗ 𑇚❗ 𑇍❗ 𑇞❗ 𑇟❗

- Sharada Supplement: --

- Siddham: 𑖃❗ 𑖙❗ 𑗊❗ 𑗋❗ 𑗌❗ 𑗍❗ 𑗎❗ 𑗏❗ 𑗐❗ 𑗑❗ 𑗒❗ 𑗓❗ 𑗔❗ 𑗕❗ 𑗖❗ 𑗗❗ 𑗘❗ 𑗉❗

- Sundanese: ᮵❗ ᮕ❗ ᮖ❗ ᮻ❗ ᮷❗ ᮿ❗ ᮌ❗ ᮍ❗ ᮙ❗ ᮾ❗ ᮺ❗ ᮠ❗ ᮐ❗ ᮓ❗ ᮏ❗

- Sundanese Supplement: ᳀❗ ᳂❗ ᳅❗ ᳆❗ ᳇❗

- Tagalog: ᜅ❗ ᜈ❗ ᜉ❗ ᜊ❗ ᜋ❗ ᜁ❗ ᜎ❗

- Tagbanwa: ᝤ❗ ᝢ❗ ᝦ❗

- Tai Le: ᥪ❗ ᥤ❗

- Tai Tham: ᪡❗ ᪣❗ ᪤❗ ᪥❗ ᪦❗ ᪬❗ ᨱ❗ ᨲ❗ ᩈ❗ ᩉ❗ ᨵ❗ ᨬ❗ ᩡ❗ ᩎ❗ 

- Takri: 𑚊❗ 𑚥❗ 𑛄❗ 

- Thai: 

- Tibetan:  

- Tirhuta: 𑒓❗ 𑒞❗ 𑓔❗ 𑓕❗ 𑒩❗ 𑒚❗ 𑒏❗

- Masaram Gondi: 𑴀❗ 𑴁❗ 𑴂❗ 𑴃❗ 𑴄❗ 𑴅❗ 𑴌❗ 𑴍❗ 𑴑❗ 𑴒❗ 𑴭❗ 𑴨❗ 𑴦❗ 𑴠❗ 𑴡❗ 

- Mro: 𖩏❗ 𖩑❗ 𖩧❗

- Ol Chiki: ᱵ❗ ᱭ❗ ᱮ❗ ᱪ❗ ᱰ❗ ᱳ❗ 

- Sora Senpeng: 𑃢❗

- Warang Citi: 𑣢❗ 𑣫❗ 𑣬❗ 𑢰❗

- Hanifi Rohingya (warning, seems right to left)

- Kayah Li: ꤥ❗ ꤮❗     

- Pahawh Hmong: 𖬂❗ 𖬕❗ 𖬄❗ 𖬈❗ 𖬩❗ 𖬤❗ 𖬸❗ 𖬷❗ 𖬻❗ 𖬼❗ 𖬽❗ 𖭄❗ 𖭅❗ 𖭒❗ 𖭓❗ 𖭕❗ 𖭗❗ 𖭘❗ 𖭜❗ 𖭝❗ 𖭟❗ 𖭠❗ 𖭧❗ 𖭦❗ 𖭩❗ 𖭪❗ 𖭫❗ 𖭬❗ 𖭷❗ 𖭿❗ 𖮂❗ 𖮊❗

- Pau Cin Hau: 𑫁❗ 𑫃❗ 𑫏❗ 𑫐❗ 𑫐❗ 𑫞❗ 𑫠❗ 𑫳❗ 𑫴❗ 𑫵❗


🝊❗ 🝭❗ ⍫❗ ⍬❗ 🝣❗ 🜸❗

- Arabic (Warning right to left):  

- Syriac Warning right to left?:  

- Georgian:   
- Georgian Extended: 

- Ethiopic script system:

- Adlam: warning, seems right-to-left 

- Bamum: 
- Bamum Supplement: 

𖥏❗ 𖠢❗ 𖡿❗ 𖠮❗ 𖡌❗ 𖡪❗ 𖡬❗ 𖡀❗
𖢿❗ 𖢧❗ 𖢨❗ 𖢶❗ 𖣇❗ 𖡣❗ 𖡁❗ 𖡂❗ 𖡘❗ 𖡙❗
𖦀❗ 𖦅❗ 𖦇❗ 𖦉❗ 𖦐❗ 𖦖❗ 𖧗❗ 𖧯❗ 𖨟❗ 𖨕❗ 𖨖❗ 𖨪❗ 𖨭❗ 𖨮❗ 𖨢❗ 𖨣❗ 𖧡❗ 𖨤❗ 𖦁❗
𖦙❗ 𖦯❗ 𖧃❗ 𖧄❗ 𖨐❗ 𖨥❗ 𖨦❗ 𖨧❗ 𖨆❗ 𖨇❗ 𖨈❗ 𖨂❗ 𖧵❗ 𖧪❗ 𖧦❗ 𖧧❗ 𖦴❗ 𖦶❗ 𖦷❗ 𖦿❗ 𖧛❗ 𖦒❗ 𖦧❗ 𖦨❗ 𖦤❗ 𖦥❗ 𖥿❗ 𖣗❗ 𖥦❗ 𖥸❗𖨐❗ 𖨥❗ 𖨦❗ 𖨧❗ 𖨆❗ 𖨇❗ 𖨈❗ 𖨂❗ 𖧵❗ 𖧪❗ 𖧦❗ 𖧧❗ 𖦴❗ 𖦶❗ 𖦷❗ 𖦿❗ 𖧛❗ 𖦒❗ 𖦧❗ 𖦨❗ 𖦤❗ 𖦥❗ 𖥿❗ 𖣗❗ 𖥦❗ 𖥸❗ 𖠷❗ 𖠪❗ 𖠹❗
𖤘❗ 𖤩❗ 𖥍❗ 𖠌❗ 𖠋❗

𖤌❗ 𖠻❗ 𖢌❗ 𖢏❗ 𖢞❗
𖢄❗:BamumS 𖣨❗ 𖥕❗ 𖤊❗ 𖤞❗ 𖥙❗ 𖥚❗ 𖣓❗ 𖣔❗ 𖣐❗ 𖣘❗ 𖣙❗ 𖣭❗
𖣵❗ 𖠑❗ 𖠟❗ 𖡹❗ 𖡦❗ 𖡨❗

𖠀❗ 𖠁❗ 𖠂❗ 𖠃❗ 𖠊❗ 𖠄❗ 𖠅❗ 𖠆❗ 𖠇❗ 𖡧❗

𖠠❗ 𖠡❗ 𖠣❗ 𖠤❗ 𖠥❗ 𖠦❗ 𖠧❗ 𖠨❗ 𖠸❗ 𖠩❗ 𖠫❗ 𖠬❗ 𖠭❗ 𖠍❗ 𖠐❗ 𖠒❗ 𖠓❗ 𖠔❗ 𖠕❗ 𖠖❗ 𖠗❗ 𖠘❗ 𖠙❗
𖡃❗ 𖡄❗ 𖡅❗ 𖡆❗ 𖡊❗ 𖡍❗ 𖡎❗ 𖡖❗ 𖡗❗ 𖡛❗ 𖡜❗ 𖡝❗ 𖡞❗ 𖡟❗ 𖡢❗ 𖡤❗ 𖡥❗ 𖡫❗ 𖡭❗ 𖡮❗ 𖡯❗
𖡰❗ 𖡱❗ 𖡲❗ 𖡳❗ 𖡴❗ 𖡵❗ 𖡷❗ 𖡸❗ 𖡽❗ 𖡾❗ 𖢁❗ 𖢂❗ 𖢃❗ 𖢅❗ 𖢆❗ 𖢇❗ 𖢈❗ 𖢉❗ 𖠰❗ 𖠱❗ 𖠲❗ 𖠳❗ 𖠴❗
𖢋❗ 𖢍❗ 𖢎❗ 𖢐❗ 𖢑❗ 𖢒❗ 𖢓❗ 𖢔❗ 𖢕❗ 𖢖❗ 𖢗❗ 𖢘❗ 𖢙❗ 𖢚❗ 𖢛❗ 𖢝❗ 𖠵❗ 𖠶❗ 𖠺❗ 𖠽❗ 𖠿❗
𖢠❗ 𖢡❗ 𖢢❗ 𖢣❗ 𖢤❗ 𖢥❗ 𖢦❗ 𖢩❗ 𖢪❗ 𖢫❗ 𖢬❗ 𖢭❗ 𖢯❗ 𖢰❗ 𖢱❗ 𖢲❗ 𖢳❗ 𖢴❗ 𖢵❗ 𖢷❗ 𖢸❗ 𖢹❗ 𖢺❗ 𖢻❗ 𖢼❗ 𖢽❗ 𖢾❗ 𖣁❗ 𖣂❗ 𖣄❗ 𖣅❗ 𖣆❗ 𖣈❗ 𖣉❗ 𖣊❗ 𖣋❗ 𖣌❗ 𖣍❗ 𖣏❗ 𖣑❗ 𖣕❗ 𖣖❗ 𖣛❗ 𖣜❗ 𖣝❗ 𖣞❗

𖣱❗ 𖣲❗ 𖣳❗ 𖣴❗ 𖣶❗ 𖣺❗ 𖣼❗ 𖣾❗ 𖣿❗ 𖤀❗ 𖤁❗ 𖤂❗ 𖤃❗ 𖤄❗ 𖤅❗ 𖤆❗ 𖤇❗ 𖤈❗ 𖤉❗ 𖤋❗ 𖤍❗ 𖤎❗
𖤑❗ 𖤒❗ 𖤓❗ 𖤕❗ 𖤖❗ 𖤗❗ 𖤙❗ 𖤚❗ 𖤛❗ 𖤜❗ 𖤝❗ 𖣡❗ 𖣢❗ 𖣤❗ 𖣥❗ 𖣦❗ 𖣧❗ 𖣩❗ 𖣪❗ 𖣫❗ 𖣬❗
𖤠❗ 𖤡❗ 𖤣❗ 𖤤❗ 𖤥❗ 𖤧❗ 𖤨❗ 𖤫❗ 𖤬❗ 𖤭❗ 𖤯❗ 𖤰❗ 𖤲❗ 𖤴❗ 𖤵❗ 𖤶❗ 𖤷❗ 𖤸❗ 𖤹❗ 𖤼❗ 𖤽❗ 𖤾❗ 𖤿❗
𖥀❗ 𖥃❗ 𖥄❗ 𖥅❗ 𖥆❗ 𖥇❗ 𖥈❗ 𖥉❗ 𖥊❗ 𖥌❗ 𖥎❗ 𖥐❗ 𖥒❗ 𖥓❗ 𖥖❗ 𖥗❗ 𖥘❗ 𖥛❗ 𖥜❗ 𖥝❗ 𖥟❗
𖥡❗ 𖥢❗ 𖥥❗ 𖥧❗ 𖥨❗ 𖥩❗ 𖥪❗ 𖥫❗ 𖥬❗ 𖥰❗ 𖥱❗ 𖥲❗ 𖥳❗ 𖥴❗ 𖥶❗ 𖥷❗ 𖥺❗ 𖥻❗ 𖥽❗ 𖥾❗ 𖠚❗ 𖠛❗
𖦂❗ 𖦃❗ 𖦄❗ 𖦈❗ 𖦍❗ 𖦎❗ 𖦕❗ 𖦘❗ 𖦚❗ 𖦜❗ 𖦞❗ 𖦟❗ 𖦠❗ 𖦢❗ 𖦣❗ 𖦦❗ 𖦩❗ 𖦪❗ 𖦫❗ 𖦬❗ 𖦭❗ 𖦮❗
𖦰❗ 𖦱❗ 𖦳❗ 𖦵❗ 𖦺❗ 𖦻❗ 𖦼❗ 𖦽❗ 𖦾❗ 𖧀❗ 𖧂❗ 𖧆❗ 𖧇❗ 𖧈❗ 𖧉❗ 𖧊❗ 𖧋❗ 𖧌❗ 𖧍❗ 𖧎❗ 𖧐❗ 𖧑❗ 𖧒❗
𖧓❗ 𖧔❗ 𖧕❗ 𖧖❗ 𖧘❗ 𖧙❗ 𖧚❗ 𖧜❗ 𖧝❗ 𖧟❗ 𖧠❗ 𖧢❗ 𖧤❗ 𖧨❗ 𖧩❗ 𖧫❗ 𖧬❗ 𖧮❗ 𖧰❗ 𖧱❗ 𖧲❗ 𖧳❗
𖧴❗ 𖧶❗ 𖧷❗ 𖧸❗ 𖧺❗ 𖧻❗ 𖧼❗ 𖧽❗ 𖧿❗ 𖨁❗ 𖨃❗ 𖨄❗ 𖨅❗ 𖨉❗ 𖨋❗ 𖨍❗ 𖨒❗ 𖨔❗ 𖨗❗ 𖨘❗ 𖨛❗ 𖨜❗
𖨝❗ 𖨞❗ 𖨨❗ 𖨩❗ 𖠜❗ 𖠝❗ 𖠞❗

𖨬❗:BamumS 𖣣❗:BammumS 𖥵❗:BamumS 𖨓❗:BamumS
𖨠❗:BamumS 𖡺❗:BamumS 𖤱❗:BamumS 𖤦❗:BamumS 𖤮❗:BamumS 𖤏❗:BamumS
𖡡❗:BamumS 𖡶❗:BamumS
𖧞❗:BamumS 𖨎❗:BamumS 𖨠❗:BamumS 𖨡❗:BamumS
𖦑❗:BamumS 𖦛❗BamumS 𖦸❗BamumS 𖦹❗:BamumS 𖦲❗:BamumS
𖦊❗:BamumS 𖦏❗:BamumS 𖦆❗:BamumS 𖣟❗:BamumS
𖥠❗:BamumS 𖥭❗:BamumS 𖥮❗:BamumS 𖥯❗:BamumS 𖥣❗:BamumS 𖥤❗:BamumS
𖥑❗:BamumS 𖥞❗:BamumS 𖥔❗:BamumS
𖣠❗:BamumS 𖣯❗:BamumS 𖣰❗:BamumS 𖤐❗:BamumS 𖤪❗:BamumS
𖥋❗:BamumS 𖥁❗:BamumS 𖤻❗:BamumS 𖤳❗:BamumS

𖡻❗:BamumS 𖡼❗:BamumS 𖣀❗:BamumS 𖢊❗:BamumS
𖣎❗:BamumS 𖢜❗:BamumS 𖡺❗:BamumS 𖡻❗:BamumS 𖡼❗:BamumS
𖦸❗:BamumS 𖦹❗:BamumS


- Bassa Vah:   𖫠❗❗:Bassa_Vah 𖫡❗❗:Bassa_Vah 𖫛❗❗:Bassa_Vah

- Medefaidrin: 



𖹓❗❗  𖹦❗❗ 𖹧❗❗ 𖹨❗❗ 𖹩❗❗ 𖹡❗❗:Medefaidrin 𖹸❗❗:Medefaidrin   𖺍❗❗:Medefaidrin 𖺙❗❗:Medefaidrin 𖺚❗❗:Medefaidrin


- Mende Kikakui: interesting, but seems right-to-left

- NKo: seems right-to-left

- Osmanya: 

- Tifinagh: 
- Vai:    

- Cyrillic:
    - Cyrillic Supplement:  
    - Cyrillic Extended A:
    - Cyrillic Extended C:
    - Cyrillic Extended D:
    - Glagolitic:      
                  	

- Tamil: 𑿁❗ 𑿂❗ 𑿈❗:Tamil_Supplement 𑿉❗ 𑿊❗ 𑿋❗ 𑿐❗ 𑿑❗:Tamil_Supplement 𑿒❗ 𑿕❗ 𑿚❗ 𑿞❗:Tamil_Supplement 𑿟❗:Tamil_Supplement 𑿠❗ 𑿯❗

- Coptic:     
Coptic Epact Numbers: 𐋮❗ 𐋴❗ 𐋺❗

- Canadian aborigenal:

ᕺ❗ ᖆ❗:Canadian ᖈ❗:Canadian ᖉ❗:Canadian ᖊ❗ ᖋ❗ ᖌ❗ ᖍ❗ ᖗ❗ ᖛ❗ ᖜ❗ ᖝ❗ ᖞ❗ ᖰ❗ ᖱ❗ ᖲ❗ ᖳ❗ ᖵ❗ ᖶ❗ ᖷ❗ ᖸ❗ ᖹ❗ ᖺ❗ ᖻ❗ ᖼ❗ ᖽ❗ ᖾ❗ ᖿ❗ ᗈ❗:Canadian  ᗆ❗:Canadian ᗐ❗:Canadian ᗑ❗:Canadian ᗒ❗:Canadian ᗓ❗ ᗔ❗ ᗕ❗:Canadian ᗜ❗ ᗝ❗ ᗟ❗ ᗠ❗ ᗡ❗ ᗢ❗ ᗣ❗ ᗤ❗ ᗥ❗ ᗦ❗ ᗧ❗ ᗨ❗ ᗭ❗ ᗮ❗ ᗲ❗ ᗵ❗ ᗶ❗ ᘎ❗:Canadian ᘏ❗:Canadian ᘔ❗:Canadian ᘕ❗:Canadian ᘚ❗ ᘛ❗ ᘢ❗ ᘣ❗ ᘤ❗:Canadian ᘧ❗:Canadian ᙅ❗:Canadian ᙂ❗:Canadian ᙀ❗:Canadian ᙁ❗:Canadian ᙎ❗:Canadian ᙏ❗:Canadian ᙐ❗ ᙑ❗ ᙓ❗:Canadian


- Cherokee:  ꚶ❗❗ ꚳ❗❗ ꚲ❗❗ ꛈ❗❗ ꛍ❗❗  ꛜ❗❗ ꛚ❗❗  ꛗ❗❗ ꛕ❗❗ ꛥ❗❗


- Deseret: 	𐐧❗ 𐐅❗  𐐃❗ 𐐏❗ 𐑏❗ 𐐱❗ 𐐜❗ 

- Osage: 𐓐❗ 𐓑❗ 𐒱❗ 𐒲❗ 𐒳❗ 𐓷❗

- Mongolian 


ᡒ❗ ᡐ❗ ᡑ❗ ᡓ❗ ᡙ❗ ᡚ❗ ᢀ❗ ᢍ❗ ᢎ❗ ᢏ❗ ᢑ❗ ᢒ❗ ᢖ❗

- runic

ᛢ❗ ᛣ❗ ᛥ❗ ᛩ❗ ᛦ❗ ᚠ❗ ᚡ❗ ᛯ❗ ᛳ❗ ᛗ❗ ᚣ❗ ᛲ❗ ᛋ❗ ᛝ❗ ᛟ❗ ᛘ❗ ᛉ❗ ᚫ❗ ᚥ❗  ᛸ❗ ᚤ❗ ᚢ❗ ᚦ❗ ᚧ❗ ᚨ❗ ᚪ❗ ᚩ❗  ᚸ❗  ᛊ❗  ᛔ❗ ᛒ❗ ᛠ❗ ᛡ❗  ᛤ❗ ᛮ❗ 	


- Chinese: 

- Hiragana:    

- Katakana:    

- Bopomofo:   
 
- Hangul syllables (built from Hangul Jamo, still each occupies 1 unicode codepoint):  


Hangul Jamo (Warning: this stuff gets merged...): ᄅ❗ ᄆ❗ ᄇ❗ ᄊ❗ ᄌ❗ ᄍ❗ ᄑ❗ ᄒ❗ ᄫ❗ ᆸ❗ ᆷ❗

Hangul Compatibility Jamo:  ㅰ❗ ㅱ❗  ㆆ❗ 

Shavian: 𐑣❗ 𐑰❗ 𐑿❗ 𐑒❗

Armenian: 

Supplemental Mathematical Operators:
 
⫏❗ ⫐❗ ⫑❗ ⫒❗ ⫓❗ ⫔❗ ⫕❗ ⫖❗ ⪪❗ ⪫❗ ⪦❗ ⪧❗ ⪨❗ ⪩❗ ⪤❗ ⫚❗ ⫛❗ ⫷❗ ⫸❗ ⫴❗ ⫵❗ ⫰❗ ⫱❗ ⫻❗ ⫼❗ ⫍❗ ⫎❗ ⪽❗ ⪾❗

Miscellaneous Mathematical Symbols-A:  

Miscellaneous Mathematical Symbols-B: ⧲❗ ⧳❗ ⧰❗ ⧱❗ ⧨❗ ⧩❗

