# CX Insights - Gucci Data Analysis

# 1. Dataframe Initialization

I began by reshaping the raw survey export into a clean, binary matrix. Each column was named using the pattern `<QuestionID>_<AnswerID>`, and each row corresponds to a single mystery shopper’s response. A value of **1** indicates the shopper selected that answer, and **0** otherwise—transforming the dataset into a fully numeric format that’s easy to analyse.

To reduce sparsity and focus on the most meaningful patterns, any answer option chosen by **fewer than 5%** of respondents was collapsed into a unified **“Other”** category. This preprocessing step greatly simplified downstream analyses by limiting the number of sparse, low-frequency columns.  

<img src="image.png" width="750px" />

# 2. Expirament 1

Next, I isolated all questions on the 5-point Likert scale and rebuilt each respondent’s score by multiplying their one-hot dummy answers by the option number (1–5) and taking the maximum. Any missing values were median-imputed, and the resulting 1–5 scores were min–max scaled into a **0–1 range** (0 = Strongly disagree → 1 = Strongly agree). 

Only the questions with a full complement of response options (no missing dummy columns) were kept for PCA. This produced a clean, continuous matrix of scaled Likert scores ready for principal‐component analysis.  

I then applied PCA to these fully-formed Likert items to uncover the key dimensions driving variation in customer sentiment. Here are the results:

<img src="image-1.png" width="750px" />



### A. Executive summary – Why PCA?

Principal Component Analysis (PCA) is a statistical technique that converts a large set of correlated survey questions into a smaller set of uncorrelated “components.”  
• It does this by finding weighted combinations of the original questions that explain the greatest amount of variation in answers.  
• The result lets us visualise patterns, segment respondents, and focus on the key drivers of the experience instead of sifting through dozens of similar‐looking questions.  
For the mystery shopping survey, PCA helps us quickly see **which aspects of the client-advisor interaction move together** and **which stand apart**, making it easier to prioritise improvements.

---

### B. What do the components mean?

| Component | Key loadings | Plain-language meaning | Suggested short name |
|-----------|--------------|------------------------|----------------------|
| **PC1** (75.2 % var.) | All five “Client-Advisor” items load strongly (+0.40 – 0.47) | A single “good vs. bad advisor experience” axis. High scores mean the shopper felt a strong connection, inspiration, and proactivity from the advisor. | “Advisor Engagement” |
| **PC2** (9.7 % var.) | “Communication was consistent throughout my journey” loads very high (+0.97) while advisor items load slightly negative | Separates perceptions of omnichannel communication consistency from the face-to-face advisor experience. High PC2 means the brand felt consistent across touch-points, regardless of how inspiring the advisor was. | “Journey Consistency” |

In short:  
• PC1 tells us **“How good was the advisor?”**  
• PC2 tells us **“How seamless was the journey’s communication?”**

<img src="image-3.png" width="750px" /> <img src="image-4.png" width="575px" />



---

### C. Four respondent segments (quadrants of the PC1 × PC2 plot)

1. **High PC1 / High PC2** – *“Luxury Loyalists”*  
   Feel both a great advisor connection and seamless brand communication.  

2. **High PC1 / Low PC2** – *“Charmed but Confused”*  
   Loved the advisor, but the wider communication felt patchy or inconsistent.  

3. **Low PC1 / High PC2** – *“Aligned but Uninspired”*  
   Found the journey coherent, yet the advisor failed to connect or inspire.  

4. **Low PC1 / Low PC2** – *“At-Risk Detractors”*  
   Experienced weak advisor engagement and disjointed communication.


<img src="image-2.png" width="650px" /> 

---

### D. Noteworthy or surprising findings

• The single “Journey – Communication consistency” item almost entirely defines PC2, showing that **omnichannel consistency is perceived independently** of the in-store advisor experience.  
• The five advisor items are so tightly correlated that they collapse into one dimension; this suggests **improving any one advisor behaviour is likely to lift the others**.

---

### E. Actionable recommendations

1. **Bridge the gap between store and digital communication.**  
   For the “Charmed but Confused” group, create a post-visit digital follow-up template that mirrors the advisor’s tone and product suggestions, ensuring the online journey feels like a continuation of the in-store experience.

2. **Focus training on inspirational storytelling.**  
   The “Aligned but Uninspired” group shows that consistency alone is not enough. Equip advisors with storytelling techniques that link individual products to the brand narrative, lifting scores on the “inspiration” and “interest” items that dominate PC1.

---

### F. Is the variance captured satisfactory?

Yes. Together, PC1 and PC2 account for **≈ 85 % of total variance**, which is more than adequate for two-dimensional visualisation and segmentation. Additional components would add only marginal insight relative to the added complexity.


# 3. Expirament 2

I focused on four key survey items:

1. **Social media channel used**  
   Which social media channel did you use? (multiple-choice)

2. **Interest uplift (Likert scale)**  
   “Based on your experience on the Gucci Social Media Channel, to what extent would you agree with:  
   _‘I felt this experience increased my interest in the products.’_”

3. **Positive drivers**  
   Please select the main reasons why the Gucci Social Media Channel **increased** your interest. (multiple-choice)

4. **Negative drivers**  
   Please select the main reasons why the Gucci Social Media Channel **did not** increase your interest. (multiple-choice)

These items include both multiple-choice flags and a 5-point Likert response. I ran PCA on this set and obtained the following results:  

### A. Executive summary  
Principal Component Analysis (PCA) is a statistical technique that compresses a wide set of possibly correlated survey variables into a small number of independent (orthogonal) “components.”  
• Why we used it here – the mystery-shopping survey contains many binary “reason” variables, channel dummies and one Likert scale.  PCA helps us:  
  1. Detect the few broad patterns that truly differentiate shoppers.  
  2. Visualise clusters/segments without looking at 20+ separate columns.  
  3. Translate the findings into clear, actionable themes for Gucci’s social-media team.  

The first three PCs already explain 70 % of the total variance, so the dimensionality of the dataset has been cut from ~15 columns to three interpretable axes with only limited information loss.  

---

### B. What the components mean  

| Component | Key high/low loadings | Plain-language meaning | Suggested name |
|-----------|-----------------------|------------------------|----------------|
| **PC1 (43 % var.)** | + Interest scale ( 0.83 )  + all positive-reason dummies ( .15–.26 )  − negative-reason dummies ( ≈ −.20 ) | Measures how strongly the interaction **raised product interest**. High scores = “I’m interested and I told you why”; low scores = “Didn’t move the needle.” | “Interest Lift” |
| **PC2 (16 % var.)** | + Instagram ( 0.57 )  − ‘Other’ channels ( −0.48 )  − positive reasons ( ≈ −.25 ) | Contrasts **Instagram-led engagement vs. non-Instagram channels**. High = Insta-first users whose interest is *not* based on rational information; low = users coming from Facebook, WeChat, etc. who rely on hard facts. | “Channel Tilt: Instagram vs. Others” |
| **PC3 (11 % var.)** | + Instagram ( 0.45 ) + positive reasons ( .20–.45 )  − Interest scale ( −0.22 ) | Captures shoppers who tick many *information* boxes and use Instagram, yet do **not report a big interest jump**. They “research a lot but stay cool.” | “Info-Hunters” |


<img src="image-7.png" width="850px" /> 
<img src="image-8.png" width="850px" />


---

### C. Four practical shop segments (using PC1 × PC2)  

| Quadrant | PC1 | PC2 | Segment nickname | Quick description |
|----------|-----|-----|------------------|-------------------|
| Q1 | + | + | **Inspired Instagram-ers** | Instagram is primary channel, high uplift in interest. Visually driven & emotionally convinced. |
| Q2 | + | − | **Detail-Oriented Discoverers** | Come from non-Instagram channels; interest rises when concrete info (availability, description) is provided. |
| Q3 | − | − | **Unconvinced Traditionalists** | Facebook/other users who did **not** gain interest; often complain about lack of clear information. |
| Q4 | − | + | **Scrolling Skeptics** | Heavy Instagram scrollers who stay indifferent—content entertains but doesn’t translate into desire. |


<img src="image-9.png" width="650px" /> <img src="image-10.png" width="650px" />

---


### D. Surprising / noteworthy findings  

1. The single Likert item (“interest scale”) dominates PC1.  In other words, **self-reported interest alone explains almost half of everything**—more than any concrete channel or content factor.  
2. Instagram is the only platform with **large, unique loadings on two different PCs (PC2 & PC3)**, indicating it creates very different sub-groups: some are thrilled (Q1), others merely scroll (Q4).  
3. Positive informational reasons *oppose* Instagram on PC2 but *align* with it on PC3.  This hints that Instagram shoppers’ motivation is often **visual/emotional first, rational second**; yet a slice of them still craves specs and storytelling (the “Info-Hunters”).  



---

### E. Actionable recommendations for Gucci’s distributor  

1. Double-layer Instagram content:  
   • Keep high-impact visuals for the “Inspired Instagram-ers.”  
   • Add a single-tap path to richer product descriptions/availability for the “Info-Hunters,” converting their curiosity into intent.  
2. For non-Instagram channels (Facebook, WeChat, etc.), surface **clear, factual information first**—price, stock status, story telling—as these details are the main drivers of interest lift in those audiences.  

---

### F. Is three components enough?  

• PC1–PC3 capture **≈ 70 %** of variability, a common heuristic for “good coverage” in consumer-research PCA.  
• The remaining 30 % is spread over ~12 minor variables, likely idiosyncratic noise (different “other” answers, small platforms).  
Conclusion: retaining three PCs is **satisfactory for strategic insights**; adding more components would yield diminishing returns and complicate the story without materially changing the recommendations.