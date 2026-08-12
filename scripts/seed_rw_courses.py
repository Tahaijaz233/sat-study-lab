import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app.database import get_db
import uuid

course = {
    'id': 'course-rw-mastery',
    'title': 'Digital SAT Reading & Writing Mastery',
    'section': 'Reading and Writing',
    'description': 'Master every domain and skill tested on the Digital SAT Reading & Writing section.'
}

modules = [
    {
        'title': 'Central Ideas and Details',
        'topic': 'Information and Ideas',
        'subtopic': 'Central Ideas and Details',
        'lecture_content': r"""# Central Ideas and Details

## Overview
Central Ideas and Details questions test your ability to read a short passage and identify the main point or a specific detail mentioned in the text. This is a foundational reading skill for the Digital SAT. In these questions, you are acting as an objective reader who simply needs to summarize what the author is saying without adding your own assumptions or outside knowledge. Every correct answer is directly supported by the text.

## Core Concepts
- **Main Idea vs. Details:** The central idea is the primary message or overarching point of the whole passage. A detail is a specific fact, piece of evidence, or example that supports the main idea.
- **Scope is Key:** Correct central idea answers must cover the entire passage, not just one sentence or paragraph. Too broad, and it includes things the passage doesn't mention. Too narrow, and it misses the overall point.
- **Literal Comprehension:** Do not read between the lines! The SAT rewards literal, exact reading. If the text doesn't say it, it's not the answer.
- **Find the Thesis:** For central idea questions, look for the "thesis statement" of the passage. It often appears in the first or last sentence.

## Worked Examples

**Example 1 (Main Idea)**
*Passage:* Many historians argue that the Industrial Revolution primarily improved the lives of the wealthy. However, a closer look at 19th-century census data reveals a significant increase in the standard of living for the middle class as well. While factory conditions were often harsh, the widespread availability of cheaper goods and new employment opportunities fostered a growing middle class that enjoyed unprecedented financial stability.

*Question:* Which choice best states the main idea of the text?
A) The Industrial Revolution had a wholly negative impact on factory workers.
B) Historical interpretations of the Industrial Revolution often ignore the wealthy.
C) The Industrial Revolution led to economic improvements for the middle class, despite some negative aspects.
D) Census data from the 19th century is often unreliable and misinterpreted.

*Step-by-step Reasoning:*
1. Read the passage carefully. The author acknowledges a common view (benefited the wealthy), introduces a contrast ("However"), and then provides evidence (census data showing middle-class improvement).
2. The core argument is that the middle class *also* benefited.
3. Evaluate the choices. (A) is too extreme and contradicts the text. (B) is false; historians argue it *did* improve the lives of the wealthy. (D) is incorrect; the author trusts the census data.
4. (C) perfectly captures the contrast and the main point: there were economic improvements for the middle class, even though conditions were sometimes harsh. Correct Answer: C.

**Example 2 (Detail)**
*Passage:* The Venus flytrap is a carnivorous plant native to subtropical wetlands on the East Coast of the United States. To thrive in nutrient-poor soil, it relies on trapping insects. When an insect brushes against the trigger hairs on the inside of the plant's leaves, the trap snaps shut. Interestingly, the trap will only close if two different hairs are stimulated within twenty seconds, a mechanism that prevents the plant from wasting energy on false alarms like falling debris.

*Question:* According to the text, what prevents a Venus flytrap from closing its trap on falling debris?
A) The presence of nutrient-poor soil in its habitat.
B) The requirement that two distinct trigger hairs be touched in quick succession.
C) The specific type of insects that are attracted to the plant.
D) The location of the trigger hairs on the outside of the leaves.

*Step-by-step Reasoning:*
1. This is a detail question. The question asks *what prevents* it from closing on falling debris.
2. Scan the text for "falling debris" or "false alarms."
3. The last sentence says: "...the trap will only close if two different hairs are stimulated within twenty seconds, a mechanism that prevents the plant from wasting energy on false alarms like falling debris."
4. Match this to the choices. (B) accurately rephrases "two different hairs are stimulated within twenty seconds." Correct Answer: B.

## Common Traps
1. **The "True but Irrelevant" Trap:** The answer choice states a fact that is true in the real world, but it is not mentioned in the text. Always stick to the passage!
2. **The "Too Narrow" Trap (for Main Idea questions):** The answer choice accurately describes a detail from the passage, but it misses the overarching point. 
3. **The "Extreme Language" Trap:** Be wary of words like *always*, *never*, *all*, *must*, or *entirely*. Passages usually contain more nuanced arguments.

## Quick Drills

**Question 1:**
*Passage:* Architect Frank Lloyd Wright believed that structures should harmonize with their environments, a philosophy he called "organic architecture." His most famous work, Fallingwater, was built directly over a waterfall, integrating the natural flow of the water and the surrounding rocks into the house's design rather than clearing the land to make way for a traditional foundation.

*Which choice best states the main idea of the text?*
A) Frank Lloyd Wright was the most influential architect of the 20th century.
B) Fallingwater is considered a masterpiece because of its traditional foundation.
C) Frank Lloyd Wright's "organic architecture" is exemplified by his design of Fallingwater.
D) Architects often struggle to build houses near waterfalls due to the challenging terrain.

**Question 2:**
*Passage:* Research on sleep patterns in teenagers suggests that their circadian rhythms naturally shift during puberty, causing them to feel awake later at night and sleepy later in the morning. Consequently, many health organizations advocate for later school start times, arguing that forcing teens to wake up early for school leads to chronic sleep deprivation, which impairs cognitive function and mood.

*According to the text, why do health organizations support later school start times?*
A) Because teenagers have more homework now than in previous decades.
B) Because early start times contribute to sleep deprivation and impaired functioning in teens.
C) Because teachers also benefit from getting more sleep in the morning.
D) Because teenagers prefer to participate in extracurricular activities late at night.

**Question 3:**
*Passage:* The discovery of penicillin by Alexander Fleming in 1928 revolutionized medicine. Before penicillin, minor cuts could easily become fatal infections. However, Fleming himself warned that the overuse of antibiotics could lead to drug-resistant bacteria. Today, this prediction has come true, as superbugs—strains of bacteria that do not respond to standard treatments—pose a major global health threat.

*Which choice best states the main idea of the text?*
A) Alexander Fleming accidentally discovered penicillin while researching other medicines.
B) While penicillin was a medical breakthrough, its overuse has led to the dangerous rise of antibiotic-resistant bacteria.
C) Superbugs are a modern invention that Alexander Fleming could never have anticipated.
D) Minor cuts are no longer considered dangerous thanks to the development of modern antibiotics.

**Answers:**
1. C
2. B
3. B
"""
    },
    {
        'title': 'Command of Evidence',
        'topic': 'Information and Ideas',
        'subtopic': 'Command of Evidence',
        'lecture_content': r"""# Command of Evidence

## Overview
Command of Evidence questions require you to evaluate how specific pieces of information (like a quote, a fact, or data from a table/graph) relate to an argument. You might be asked to find evidence that *supports* a claim, evidence that *weakens* a claim, or to draw a conclusion based on provided quantitative data. These questions test your critical thinking and logical reasoning skills.

## Core Concepts
- **Identify the Claim First:** Before looking at the answers, isolate the exact claim or hypothesis being tested. What is the researcher arguing? What is the core hypothesis?
- **Direction of Evidence:** Determine whether you need to *support* (strengthen, confirm) or *weaken* (undermine, challenge) the claim.
- **Support = Same Idea:** To support a claim, the correct answer must provide an example, statistic, or fact that aligns perfectly with the claim's logic.
- **Weaken = Contradiction:** To weaken a claim, the correct answer must provide information that shows the claim is flawed, incomplete, or incorrect.
- **Data Literacy:** When given a chart or graph, read the title, axes, and legend carefully. Don't make assumptions—only use the data explicitly provided.

## Worked Examples

**Example 1 (Textual Evidence - Support)**
*Passage:* Biologist Dr. Aris asserts that certain species of urban birds have adapted their songs to be heard over city noise. Specifically, she hypothesizes that birds living in environments with high levels of low-frequency traffic noise will sing at a higher pitch than those of the same species living in quiet rural areas.

*Question:* Which finding, if true, would most directly support Dr. Aris's hypothesis?
A) Urban birds are found to sing louder than rural birds, regardless of the pitch of their songs.
B) A study shows that the songs of rural birds are more complex than the songs of urban birds.
C) Measurements reveal that urban birds sing at significantly higher frequencies than their rural counterparts.
D) Traffic noise in urban areas has been steadily increasing over the past decade.

*Step-by-step Reasoning:*
1. Identify the claim: Urban birds sing at a *higher pitch* than rural birds because of low-frequency city noise.
2. Goal: Support the hypothesis.
3. Evaluate choices. (A) talks about loudness, not pitch. (B) talks about complexity, not pitch. (D) talks about noise increasing, but doesn't mention bird songs.
4. (C) directly states that urban birds sing at higher frequencies (which means higher pitch) than rural birds. This perfectly matches the hypothesis. Correct Answer: C.

**Example 2 (Quantitative Evidence)**
*Passage:* A company tested the durability of three different materials for a new smartphone screen: Glass A, Glass B, and Plastic C. They dropped phones with these screens from various heights and recorded the percentage of screens that cracked. The engineers claimed that Glass B is the most durable material for drops from 5 feet or higher.

*(Imagine a table showing cracking percentages at 5 feet: Glass A = 40%, Glass B = 10%, Plastic C = 15%)*

*Question:* Which choice provides data from the table that best supports the engineers' claim?
A) Glass A had a 40% cracking rate at 5 feet, which is higher than Plastic C.
B) At a drop height of 5 feet, Glass B had the lowest cracking rate at only 10%.
C) Plastic C cracked 15% of the time, making it less durable than Glass A.
D) Glass B is heavier than both Glass A and Plastic C, contributing to its durability.

*Step-by-step Reasoning:*
1. Identify the claim: Glass B is the *most durable* (least likely to crack) from 5 feet.
2. Look at the data: At 5 feet, Glass B is 10%, A is 40%, C is 15%.
3. Goal: Find the choice that uses this data to support the claim.
4. (B) explicitly uses the correct data (10%) and confirms it was the lowest cracking rate, supporting the idea that it's the most durable. Correct Answer: B.

## Common Traps
1. **The "Opposite" Trap:** You are asked to strengthen a claim, but the answer choice weakens it (or vice versa). Always double-check what the question is asking!
2. **The "Irrelevant Evidence" Trap:** The choice provides a true statement or accurate data from the chart, but it doesn't actually address the specific claim in question.
3. **The "Half-Right" Trap:** The choice starts by addressing the claim but ends with an incorrect interpretation of the data or passage.

## Quick Drills

**Question 1:**
*Passage:* Historian Jane Doe argues that the decline of the ancient city of Teotihuacan was primarily caused by internal social uprisings rather than foreign invasions. She points to evidence of destruction focused heavily on the temples and residences of the ruling class, while commoner neighborhoods remained largely untouched.

*Which finding, if true, would most weaken Doe’s argument?*
A) New excavations reveal that weapons found in the destroyed elite residences were definitively made by a rival foreign empire.
B) Records indicate that the ruling class of Teotihuacan imposed heavy taxes on the commoners.
C) Similar patterns of destruction were found in other ancient cities that experienced internal revolutions.
D) The commoner neighborhoods were located further away from the city center than the elite residences.

**Question 2:**
*Passage:* Some agricultural scientists claim that using organic farming methods exclusively will result in a global food shortage because organic yields are significantly lower than conventional yields per acre.

*Which finding, if true, would most directly challenge the scientists' claim?*
A) Consumers are willing to pay higher prices for organically grown produce.
B) Recent advancements in organic pest control have brought organic crop yields to levels matching or exceeding conventional farming yields.
C) Conventional farming methods often rely on synthetic fertilizers that can deplete soil quality over time.
D) The amount of arable land available for farming is decreasing worldwide due to urbanization.

**Question 3:**
*Passage:* A researcher hypothesizes that exposure to blue light from screens before bed suppresses the production of melatonin, a hormone that regulates sleep, leading to an increase in the time it takes to fall asleep.

*Which finding, if true, would most directly support the researcher's hypothesis?*
A) Participants who read a physical book before bed reported having more vivid dreams.
B) A study found that participants who used smartphones for an hour before bed took 45 minutes longer to fall asleep and had lower melatonin levels than those who did not.
C) Blue light glasses are marketed as a way to reduce eye strain for office workers.
D) Melatonin supplements are commonly used to treat jet lag in travelers.

**Answers:**
1. A
2. B
3. B
"""
    },
    {
        'title': 'Information and Ideas',
        'topic': 'Information and Ideas',
        'subtopic': 'Information and Ideas',
        'lecture_content': r"""# Information and Ideas (General Inference)

## Overview
General inference questions on the Digital SAT ask you to draw a logical conclusion based *only* on the information provided in the passage. These questions are essentially logic puzzles. The passage will give you a set of premises (facts), and you must determine what must be true as a result. Crucially, the correct answer is never explicitly stated word-for-word in the text, but it is inescapably true based on the text.

## Core Concepts
- **Strict Logic:** Inference on the SAT is not about guessing the author's hidden feelings. It's about deduction. If A = B and B = C, then A = C.
- **The "No Outside Knowledge" Rule:** Never bring in outside facts. If the passage says the sky is green, then for the purpose of the question, the sky is green.
- **Connecting the Dots:** Often, the passage will present two pieces of information separated by a few sentences. The correct answer will synthesize these two pieces of information.
- **Tone Down the Certainty:** Correct inference answers often use soft language like *may*, *might*, *suggests*, *can be*, or *some*. Answers with extreme language (*always*, *must*, *proves*, *all*) are very hard to prove with the given text and are usually wrong.

## Worked Examples

**Example 1**
*Passage:* In the late 19th century, the demand for natural rubber skyrocketed due to the invention of the pneumatic tire. At the time, the rubber tree (*Hevea brasiliensis*) was only found in the Amazon rainforest. However, a British explorer smuggled thousands of rubber tree seeds out of Brazil and planted them in Southeast Asia. Today, the vast majority of the world's natural rubber is produced in Southeast Asia, not South America.

*Question:* Based on the text, what can be reasonably inferred about the production of natural rubber?
A) The climate in Southeast Asia is more suitable for growing rubber trees than the climate in the Amazon.
B) If the British explorer had not smuggled the seeds, the Amazon would still be the sole producer of natural rubber.
C) The rubber trees currently growing in Southeast Asia are descendants of the trees originating in the Amazon rainforest.
D) The pneumatic tire was invented specifically to increase the demand for natural rubber.

*Step-by-step Reasoning:*
1. Read for facts: Rubber was originally *only* in the Amazon. Seeds were taken from Brazil to SE Asia. Now, SE Asia produces most of the rubber.
2. Evaluate choices based *strictly* on the text. (A) assumes climate is the reason; the text doesn't say that (maybe it's cheaper labor or better farming). (B) uses a hypothetical "what if"—we can't know for sure. (D) is factually backwards and unsupported.
3. Look at (C). The text says the trees were *only* in the Amazon, and seeds were taken to SE Asia to start production. Therefore, the trees in SE Asia must be descendants of those original seeds. This is a solid deduction. Correct Answer: C.

**Example 2**
*Passage:* Some species of frogs in environments with unpredictable rainfall have developed a rapid developmental cycle. While a typical tadpole might take weeks to metamorphose into a frog, the tadpoles of the spadefoot toad can complete the process in just a few days if their temporary breeding pools begin to dry up.

*Question:* It can be reasonably inferred from the text that the rapid developmental cycle of the spadefoot toad tadpole is...
A) a disadvantage when competing with typical tadpoles for food.
B) an adaptation that increases their chances of survival in temporary water sources.
C) caused by the high temperatures typically found in unpredictable environments.
D) unique among all amphibian species.

*Step-by-step Reasoning:*
1. Facts: Unpredictable rainfall -> rapid cycle. Spadefoot toad tadpoles morph in days *if pools begin to dry up*.
2. Connect the dots: Drying pools would kill a tadpole. Metamorphosing quickly gets them out of the drying pool.
3. Evaluate choices. (A) mentions food competition, which isn't in the text. (C) mentions high temperatures, not in the text. (D) says "unique among *all*," which is too extreme.
4. (B) perfectly captures the logic: it helps them survive when the water source is temporary (drying up). Correct Answer: B.

## Common Traps
1. **The "Plausible but Unproven" Trap:** The answer makes sense in the real world, but the passage doesn't provide enough evidence to prove it.
2. **The Extreme Language Trap:** Watch out for words like *never*, *always*, *completely*, or *proves*. Inference answers usually need to be milder.
3. **The Reversal Trap:** The answer gets the relationship backwards (e.g., confusing cause and effect).

## Quick Drills

**Question 1:**
*Passage:* Although most meteors burn up completely in Earth's atmosphere, forming "shooting stars," some larger fragments survive the fiery descent and strike the ground. These surviving fragments are known as meteorites. Interestingly, the vast majority of meteorites found on Earth contain high levels of iron and nickel, unlike typical terrestrial rocks.

*Based on the text, what can be reasonably inferred about a rock found on Earth that lacks high levels of iron and nickel?*
A) It is likely not a meteorite.
B) It burned up completely in the atmosphere.
C) It is older than most typical terrestrial rocks.
D) It originated from a different solar system.

**Question 2:**
*Passage:* The city of Pompeii was buried under volcanic ash when Mount Vesuvius erupted in 79 AD. Because the ash sealed the city instantly, it prevented moisture and air from reaching the structures. As a result, historians have been able to study perfectly preserved loaves of bread, colorful frescoes, and even wooden furniture that would have otherwise decayed centuries ago.

*What can be inferred about the decay of wooden furniture?*
A) It is usually caused by exposure to intense heat and volcanic ash.
B) It generally requires the presence of moisture and air.
C) It happens much faster in ancient cities than in modern ones.
D) It was prevented in Pompeii primarily because the furniture was made of special wood.

**Question 3:**
*Passage:* In many corporate environments, managers believe that holding frequent, long meetings increases productivity by ensuring everyone is aligned. However, recent surveys of employees indicate that spending more than four hours a week in meetings significantly reduces their ability to complete actual tasks, leading to missed deadlines and increased stress.

*It can be reasonably inferred from the text that...*
A) Managers do not care about employee stress levels.
B) Employees would prefer to communicate solely through email.
C) There is a disconnect between management's expectations of meetings and their actual impact on task completion.
D) Companies that ban meetings entirely are the most productive.

**Answers:**
1. A
2. B
3. C
"""
    },
    {
        'title': 'Words in Context',
        'topic': 'Craft and Structure',
        'subtopic': 'Words in Context',
        'lecture_content': r"""# Words in Context

## Overview
Words in Context questions ask you to select the most logical and precise word or phrase to fill in a blank within a passage. These questions do not merely test your vocabulary; they test your ability to read carefully and use context clues to determine the exact meaning required by the sentence.

## Core Concepts
- **Cover and Predict:** Before looking at the answer choices, cover them up. Read the passage and come up with your own word for the blank based on the context. Then, find the choice that matches your prediction.
- **Find the Clue:** Every Words in Context passage contains a specific word or phrase that serves as a "clue" for what the blank must mean. Look for definitions, synonyms, or contrasts within the text itself.
- **Identify the Direction (Transition):** Look for transition words. Words like *and*, *similarly*, or *because* indicate that the blank will agree with the clue. Words like *but*, *however*, or *despite* indicate that the blank will contrast with the clue.
- **Precision Matters:** Sometimes multiple answer choices kind of make sense. You must choose the one that is the *most precise* fit for the specific context provided by the author.

## Worked Examples

**Example 1**
*Passage:* The documentary director was known for her _____ approach to filmmaking; she would spend years meticulously researching a subject, refusing to release a film until she was certain every single detail was historically accurate.

*Question:* Which choice completes the text with the most logical and precise word or phrase?
A) hasty
B) exacting
C) indifferent
D) unconventional

*Step-by-step Reasoning:*
1. Cover the choices. What goes in the blank? A word describing her approach.
2. Find the clue: "meticulously researching," "refusing to release... until certain every single detail was historically accurate."
3. The clue means careful, strict, and precise.
4. Look at the choices. (A) *hasty* means rushed (opposite). (C) *indifferent* means uncaring (opposite). (D) *unconventional* means weird/unusual (not the focus).
5. (B) *exacting* means making great demands on one's skill, attention, or other resources; being precise. This matches perfectly. Correct Answer: B.

**Example 2**
*Passage:* Despite the initial excitement surrounding the new software launch, the program was riddled with bugs, causing the company's stock price to plummet. In an attempt to _____ investors, the CEO held an emergency press conference to outline a clear timeline for fixing the issues.

*Question:* Which choice completes the text with the most logical and precise word or phrase?
A) alienate
B) placate
C) bewilder
D) mimic

*Step-by-step Reasoning:*
1. The company's stock plummeted and the software has bugs. Investors are likely angry or panicked.
2. The CEO is outlining a plan to fix the issues. Why? To calm the investors down.
3. Prediction for the blank: "calm," "soothe," or "reassure."
4. Evaluate the choices. (A) *alienate* means to push away. (C) *bewilder* means to confuse. (D) *mimic* means to copy.
5. (B) *placate* means to make someone less angry or hostile. This fits the prediction perfectly. Correct Answer: B.

## Common Traps
1. **The "Sounds Smart but Wrong Meaning" Trap:** The SAT will often include advanced vocabulary words that look correct because they are difficult, but their actual definition doesn't fit the context.
2. **The "Related but Imprecise" Trap:** The word is related to the topic of the sentence, but it doesn't fit the specific logic. (e.g., using "financial" when you need "frugal").
3. **Ignoring the Contrast:** Missing a "despite" or "however" and choosing a synonym instead of an antonym.

## Quick Drills

**Question 1:**
*Passage:* The artist's early paintings were praised for their vibrant colors and bold, expressive strokes. However, her later works were heavily criticized for being overly _____, lacking the emotion and spontaneity that had characterized her initial success.

*Which choice completes the text with the most logical and precise word or phrase?*
A) derivative
B) passionate
C) mechanical
D) controversial

**Question 2:**
*Passage:* The sheer volume of data collected by the telescope was so _____ that the research team had to develop a new artificial intelligence program just to sort through the initial findings.

*Which choice completes the text with the most logical and precise word or phrase?*
A) trivial
B) manageable
C) overwhelming
D) theoretical

**Question 3:**
*Passage:* Because the ancient manuscript was extremely fragile and the ink was fading rapidly, the scholars handled the document with the utmost _____, ensuring the room's humidity and lighting were perfectly controlled.

*Which choice completes the text with the most logical and precise word or phrase?*
A) reverence
B) hostility
C) skepticism
D) haste

**Answers:**
1. C (The contrast is against "emotion and spontaneity." "Mechanical" means lacking emotion or spontaneity.)
2. C
3. A
"""
    },
    {
        'title': 'Craft and Structure',
        'topic': 'Craft and Structure',
        'subtopic': 'Craft and Structure',
        'lecture_content': r"""# Craft and Structure (Text Structure, Purpose, Cross-Text)

## Overview
This category covers three distinct but related types of questions. 
1. **Text Structure:** How does the passage flow? (e.g., from a general claim to a specific example).
2. **Text Purpose:** Why did the author write the text? What is their main goal?
3. **Cross-Text Connections (Paired Passages):** Comparing two short passages on the same topic to determine how the authors agree or disagree.

These questions ask you to look at the text structurally and rhetorically, focusing on *how* the text is built rather than just *what* it says.

## Core Concepts
- **Structural Shifts:** Pay attention to transition words (*however*, *for example*, *ultimately*). A passage often shifts from setting the scene -> posing a problem -> offering a solution.
- **Main Purpose vs. Main Idea:** Main Idea = What the text says. Main Purpose = What the text *does* (e.g., *to criticize*, *to explain*, *to argue*). The correct purpose must apply to the *entire* passage.
- **Cross-Text Strategy:** For dual passages, read Text 1 and summarize its main point. Read Text 2 and summarize its main point. Then, explicitly ask yourself: "Do they agree, disagree, or focus on different aspects of the same topic?"

## Worked Examples

**Example 1 (Text Purpose)**
*Passage:* While many consumers believe that recycling plastic is a perfect solution to environmental pollution, the reality is far more complex. Most municipal recycling facilities are only equipped to handle type 1 and type 2 plastics. Furthermore, the process of recycling plastic often degrades the material, meaning it can only be repurposed a limited number of times before ending up in a landfill. Therefore, reducing plastic consumption at the source is a far more effective strategy than relying solely on recycling.

*Question:* Which choice best states the main purpose of the text?
A) To describe the technical process of recycling type 1 and type 2 plastics.
B) To argue that reducing plastic consumption is superior to relying on recycling.
C) To criticize consumers for their ignorance about environmental pollution.
D) To advocate for increased funding for municipal recycling facilities.

*Step-by-step Reasoning:*
1. Read the text and look for the author's primary goal. The author introduces a common belief (recycling is perfect), points out flaws (only handles certain types, degrades material), and offers a conclusion (reducing consumption is better).
2. The overall goal is to convince the reader of that final point.
3. Evaluate choices. (A) is too narrow—it barely mentions the process. (C) is too aggressive; the author corrects consumers but doesn't "criticize" them harshly. (D) is not mentioned in the text.
4. (B) perfectly captures the overarching argument the author is making. Correct Answer: B.

**Example 2 (Cross-Text Connections)**
*Text 1:* The gig economy, characterized by freelance work and short-term contracts, offers workers unprecedented flexibility. Drivers and delivery workers can set their own hours, allowing them to balance work with family obligations or education in a way that traditional 9-to-5 jobs do not allow.

*Text 2:* Proponents of the gig economy often praise its flexibility, but they ignore the severe lack of worker protections. Gig workers are generally classified as independent contractors, meaning they do not receive health insurance, paid sick leave, or a guaranteed minimum wage, leaving them highly vulnerable to economic instability.

*Question:* Based on the texts, how would the author of Text 2 most likely respond to the claims made in Text 1?
A) By agreeing that flexibility is the most important factor for modern workers.
B) By arguing that traditional 9-to-5 jobs are becoming obsolete.
C) By pointing out that the flexibility mentioned in Text 1 comes at the cost of essential worker protections.
D) By suggesting that gig workers should form unions to negotiate better hours.

*Step-by-step Reasoning:*
1. Summarize Text 1: Gig economy is good because it gives workers flexibility.
2. Summarize Text 2: The gig economy is bad because, despite the flexibility, workers lack basic protections (insurance, minimum wage).
3. Look at the relationship: Text 2 acknowledges Text 1's point (flexibility) but argues that the downside (lack of protection) is a major problem.
4. Find the matching choice. (C) perfectly captures this dynamic. Correct Answer: C.

## Common Traps
1. **The "True but Wrong Purpose" Trap:** The answer choice accurately describes something that happens in the text, but it's not the *main purpose* of the text as a whole.
2. **The Misaligned Comparison:** In cross-text questions, choosing an answer that is true for Text 1 but doesn't reflect the view of Text 2 (or vice versa).

## Quick Drills

**Question 1:**
*Passage:* The concept of "rewilding"—restoring habitats to their natural state and reintroducing apex predators—has gained traction in recent years. In Yellowstone National Park, the reintroduction of wolves in 1995 controlled the overpopulated elk herds. This allowed overgrazed willow and aspen trees to recover along riverbanks, which in turn provided materials for beavers to build dams, ultimately creating healthier wetland ecosystems.

*Which choice best describes the overall structure of the text?*
A) It introduces a controversial theory and then provides evidence to debunk it.
B) It defines a conservation strategy and then provides a specific example of its cascading positive effects.
C) It compares the ecosystems of two different national parks to highlight the importance of apex predators.
D) It outlines a historical event and then criticizes the scientists involved for their lack of foresight.

**Question 2:**
*Text 1:* The implementation of a four-day workweek in a New Zealand trust management company resulted in a 20% increase in employee productivity. Workers reported feeling more rested and motivated, proving that working fewer hours can actually benefit a company's bottom line.

*Text 2:* While some isolated case studies show positive results from a four-day workweek, applying this model universally is impractical. In industries like healthcare, manufacturing, and customer service, businesses must operate 24/7. Reducing employee hours in these sectors would require hiring significantly more staff, drastically increasing labor costs.

*Based on the texts, both authors would most likely agree with which statement?*
A) The four-day workweek will eventually become the standard for all industries.
B) Employee productivity is the most important metric for business success.
C) A four-day workweek can have a measurable impact on a business's operations.
D) The healthcare industry is fundamentally flawed in its management of employee hours.

**Question 3:**
*Passage:* When jazz trumpeter Miles Davis released the album *Kind of Blue* in 1959, he abandoned the dense chord progressions typical of bebop in favor of "modal jazz." In modal jazz, musicians improvise based on scales (modes) rather than rapidly changing chords. This approach created a spacious, relaxed sound that allowed for more melodic freedom, making *Kind of Blue* one of the most critically acclaimed and best-selling jazz albums of all time.

*Which choice best states the main purpose of the text?*
A) To argue that modal jazz is superior to bebop.
B) To explain how a specific musical innovation contributed to the success of a landmark album.
C) To detail the biographical history of Miles Davis's early career.
D) To criticize the dense chord progressions used in traditional bebop music.

**Answers:**
1. B
2. C (Text 1 sees a positive impact; Text 2 sees a negative impact/cost. Both agree it impacts operations).
3. B
"""
    },
    {
        'title': 'Transitions',
        'topic': 'Expression of Ideas',
        'subtopic': 'Transitions',
        'lecture_content': r"""# Transitions

## Overview
Transition questions ask you to choose the most logical word or phrase to connect two sentences or clauses. The transition must accurately reflect the logical relationship between the ideas presented. These are some of the most common and predictable questions on the SAT Writing section.

## Core Concepts
- **Read Around the Blank:** To find the relationship, you must read the sentence *before* the blank and the sentence containing the blank.
- **Determine the Relationship:** There are three main types of relationships:
    1.  **Continuers (Addition/Similarity/Example):** The second sentence adds information, gives an example, or continues the same thought. *Transitions: Furthermore, In addition, For example, Similarly, Indeed.*
    2.  **Contradictors (Contrast/Opposition):** The second sentence disagrees with, limits, or contrasts with the first. *Transitions: However, Nevertheless, On the other hand, Conversely, Despite this.*
    3.  **Cause and Effect (Result):** The first sentence causes the second, or the second is a logical conclusion of the first. *Transitions: Therefore, Consequently, As a result, Thus, Accordingly.*
- **The "Blank Test":** Try reading the two sentences *without* any transition word. Ask yourself: Are these sentences agreeing, disagreeing, or is one causing the other?

## Worked Examples

**Example 1**
*Passage:* In 1912, Alfred Wegener proposed the theory of continental drift, suggesting that the Earth's continents had once been a single supercontinent. _____, his ideas were largely rejected by the scientific community because he could not explain the mechanism by which the continents moved.

*Question:* Which choice completes the text with the most logical transition?
A) Furthermore
B) However
C) For example
D) As a result

*Step-by-step Reasoning:*
1. Sentence 1: Wegener proposed a major scientific theory. (Positive/Neutral)
2. Sentence 2: His ideas were rejected by the scientific community. (Negative)
3. The relationship is a contrast. He proposed it, *but* it was rejected.
4. Evaluate choices: (A) is a continuer. (C) is for an example. (D) is cause/effect (proposing a theory doesn't cause it to be rejected).
5. (B) *However* perfectly captures the contrast. Correct Answer: B.

**Example 2**
*Passage:* The city of Tokyo has invested heavily in public transportation infrastructure over the last few decades, developing one of the most efficient train networks in the world. _____, the rate of car ownership in the city has steadily declined as residents find it faster and cheaper to commute via rail.

*Question:* Which choice completes the text with the most logical transition?
A) Consequently
B) Nevertheless
C) Similarly
D) Previously

*Step-by-step Reasoning:*
1. Sentence 1: Tokyo built an amazing, efficient train network.
2. Sentence 2: Car ownership declined because residents commute via rail.
3. What is the relationship? Building the train network *caused* the decline in car ownership.
4. Evaluate choices: (B) is contrast. (C) is comparison. (D) is time.
5. (A) *Consequently* indicates cause and effect. Correct Answer: A.

## Common Traps
1. **The "Sound Good" Trap:** Choosing a transition just because it sounds nice in the sentence without analyzing the logical relationship.
2. **False Contrast:** Using "However" when the sentences are actually agreeing with each other.
3. **Double Transitions:** Be careful if the second sentence already has a transition word later in the sentence (though rare on the Digital SAT, it happens).

## Quick Drills

**Question 1:**
*Passage:* Many people assume that deserts are entirely lifeless expanses of sand. _____, deserts are home to a wide variety of highly adapted plants and animals, such as the saguaro cactus and the fennec fox, which thrive in arid conditions.

*Which choice completes the text with the most logical transition?*
A) In fact
B) Similarly
C) Therefore
D) For instance

**Question 2:**
*Passage:* To bake a perfect soufflé, a chef must meticulously whip the egg whites to create microscopic air bubbles. _____, the chef must fold the egg whites into the base very gently to ensure those air bubbles do not collapse.

*Which choice completes the text with the most logical transition?*
A) On the contrary
B) Subsequently
C) In contrast
D) For example

**Question 3:**
*Passage:* The marketing team launched a massive social media campaign to promote the new smartphone, spending millions on influencer partnerships. _____, sales of the device were dismally low during the first quarter.

*Which choice completes the text with the most logical transition?*
A) Thus
B) In addition
C) Nevertheless
D) Specifically

**Answers:**
1. A (Contrasting the assumption with the reality).
2. B ("Subsequently" means "next" or "afterwards," showing a sequence of steps).
3. C (Contrast: spent millions, *but* sales were low).
"""
    },
    {
        'title': 'Expression of Ideas',
        'topic': 'Expression of Ideas',
        'subtopic': 'Expression of Ideas',
        'lecture_content': r"""# Expression of Ideas (Rhetorical Synthesis)

## Overview
Rhetorical Synthesis questions are unique to the Digital SAT. You will be given a bulleted list of notes taken by a student. You must then choose the sentence that best uses that information to accomplish a specific, stated goal. 

## Core Concepts
- **Identify the Goal:** This is the most important step! Read the question carefully to find the specific rhetorical goal. Examples of goals: "Emphasize a similarity," "Contrast two things," "Introduce an author and their book," or "Explain a cause-and-effect relationship."
- **Be Ruthless:** The correct answer MUST accomplish the stated goal. Even if an answer choice contains accurate information from the notes, if it does not achieve the specific goal, it is wrong.
- **Ignore the Notes (Mostly):** You usually don't need to read the bulleted notes carefully. The notes just provide the raw facts. Focus heavily on matching the answer choices to the goal in the question prompt.

## Worked Examples

**Example 1**
*Passage:* While researching a topic, a student has taken the following notes:
- The blobfish (*Psychrolutes marcidus*) lives in deep ocean waters off the coasts of Australia and New Zealand.
- At these depths, the water pressure is 60 to 120 times greater than at sea level.
- The blobfish lacks a swim bladder and has gelatinous flesh with a density slightly less than water.
- This adaptation allows it to float above the sea floor without expending energy on swimming.
- When brought to the surface, the lack of pressure causes its gelatinous body to expand and collapse, giving it a "blob" appearance.

*Question:* The student wants to explain **why the blobfish looks like a "blob" when brought to the surface**. Which choice most effectively uses relevant information from the notes to accomplish this goal?
A) The blobfish, which lives off the coasts of Australia and New Zealand, has a density slightly less than water, allowing it to float.
B) Because it lives at extreme ocean depths, the blobfish has adapted by developing gelatinous flesh rather than a swim bladder.
C) When removed from the extreme high pressure of its deep-sea habitat, the blobfish's gelatinous body loses its structural support and collapses.
D) The blobfish is well-adapted to extreme pressure, allowing it to survive where the pressure is 60 to 120 times greater than at sea level.

*Step-by-step Reasoning:*
1. **Identify the goal:** Explain *why* it looks like a blob at the surface.
2. Evaluate (A): Explains floating, doesn't mention the surface or the blob appearance.
3. Evaluate (B): Explains adaptation to depth, doesn't mention the surface appearance.
4. Evaluate (C): Directly explains the cause (removed from high pressure) and effect (gelatinous body collapses), answering *why* it looks like a blob at the surface.
5. Evaluate (D): Explains survival at deep depths, not surface appearance.
6. Correct Answer: C.

**Example 2**
*Passage:* While researching a topic, a student has taken the following notes:
- Frida Kahlo was a Mexican painter known for her many portraits, self-portraits, and works inspired by the nature and artifacts of Mexico.
- She often mixed realism with fantasy in her art.
- Diego Rivera was a prominent Mexican painter.
- His large frescoes helped establish the Mexican mural movement in Mexican and international art.
- Kahlo and Rivera were married and had a volatile relationship, but they deeply influenced each other's art.

*Question:* The student wants to **emphasize a difference between the artistic styles** of Kahlo and Rivera. Which choice most effectively uses relevant information from the notes to accomplish this goal?
A) Both Frida Kahlo and Diego Rivera were highly influential Mexican painters whose relationship impacted their art.
B) While Kahlo is famous for her intimate portraits and self-portraits that blended realism with fantasy, Rivera is renowned for his massive public frescoes.
C) Kahlo, known for her self-portraits, was married to Diego Rivera, a leading figure in the Mexican mural movement.
D) Kahlo's work was inspired by the nature and artifacts of Mexico, much like the work of other prominent artists of her time.

*Step-by-step Reasoning:*
1. **Identify the goal:** Emphasize a *difference* between their *artistic styles*.
2. Evaluate (A): Emphasizes a similarity and their relationship. Wrong goal.
3. Evaluate (B): Contrasts Kahlo's style (intimate portraits, fantasy/realism) with Rivera's style (massive public frescoes). Achieves the goal perfectly.
4. Evaluate (C): Mentions both artists, but doesn't explicitly contrast their styles. It just states facts.
5. Evaluate (D): Only talks about Kahlo.
6. Correct Answer: B.

## Common Traps
1. **The "True but Unhelpful" Trap:** An answer choice that is 100% factually accurate based on the notes, but completely ignores the specific goal asked in the prompt.
2. **Missing the Focus:** The goal asks to emphasize a *similarity*, but the student chooses an answer that emphasizes a *difference*.

## Quick Drills

**Question 1:**
*Notes:*
- The planet Venus has a thick atmosphere composed primarily of carbon dioxide.
- This thick atmosphere creates a runaway greenhouse effect.
- The surface temperature on Venus can reach 900 degrees Fahrenheit (475 degrees Celsius).
- Mercury is the closest planet to the Sun.
- Despite being further from the Sun, Venus is hotter than Mercury.

*Goal:* The student wants to **explain the cause of Venus's extreme surface temperature**. Which choice most effectively uses relevant information from the notes to accomplish this goal?
A) Venus is actually hotter than Mercury, even though Mercury is the closest planet to the Sun.
B) The surface temperature on Venus can reach an astonishing 900 degrees Fahrenheit.
C) A runaway greenhouse effect, caused by a thick carbon dioxide atmosphere, drives Venus's surface temperatures up to 900 degrees Fahrenheit.
D) Venus has a thick atmosphere made mostly of carbon dioxide, while Mercury is much closer to the Sun.

**Question 2:**
*Notes:*
- *The Great Gatsby* is a 1925 novel written by F. Scott Fitzgerald.
- It is set in the "Roaring Twenties" in Long Island, New York.
- The novel explores themes of decadence, idealism, and the American Dream.
- Upon its initial publication, the novel received mixed reviews and sold poorly.
- Today, it is considered a literary masterwork and a contender for the title of the "Great American Novel."

*Goal:* The student wants to **contrast the initial reception of *The Great Gatsby* with its modern reputation**. Which choice most effectively uses relevant information from the notes to accomplish this goal?
A) Set in the Roaring Twenties, F. Scott Fitzgerald's *The Great Gatsby* explores themes of decadence and the American Dream.
B) Although F. Scott Fitzgerald's 1925 novel *The Great Gatsby* received mixed reviews and sold poorly upon release, it is now widely celebrated as a literary masterwork.
C) *The Great Gatsby* initially received mixed reviews, which was disappointing for the author F. Scott Fitzgerald.
D) Today, *The Great Gatsby* is considered a contender for the title of the "Great American Novel," exploring themes of idealism.

**Question 3:**
*Notes:*
- Marie Curie discovered the elements polonium and radium.
- She was the first woman to win a Nobel Prize.
- She is the only person to win a Nobel Prize in two different scientific fields (Physics in 103, Chemistry in 1911).
- She coined the term "radioactivity."

*Goal:* The student wants to **highlight Marie Curie's unique achievements regarding the Nobel Prize**. Which choice most effectively uses relevant information from the notes to accomplish this goal?
A) Marie Curie, who coined the term "radioactivity," discovered the elements polonium and radium.
B) In addition to discovering polonium and radium, Marie Curie was a pioneer in the study of radioactivity.
C) Marie Curie was not only the first woman to win a Nobel Prize, but she also remains the only person to win the award in two different scientific fields.
D) Marie Curie won her first Nobel Prize in Physics in 1903 and her second in Chemistry in 1911.

**Answers:**
1. C (Explains the *cause*—greenhouse effect/atmosphere).
2. B (Explicitly contrasts the past failure with modern success).
3. C (Focuses precisely on her unique Nobel Prize milestones).
"""
    },
    {
        'title': 'Boundaries and Sentence Structure',
        'topic': 'Standard English Conventions',
        'subtopic': 'Boundaries and Sentence Structure',
        'lecture_content': r"""# Boundaries and Sentence Structure

## Overview
Sentence boundaries test your ability to correctly link or separate independent and dependent clauses. You need to know how to use periods, semicolons, colons, dashes, and conjunctions to prevent run-on sentences, comma splices, and sentence fragments.

## Core Concepts
- **Independent Clause (IC):** A complete thought with a subject and a working verb. It can stand alone as a sentence. (e.g., *The dog barked.*)
- **Dependent Clause (DC):** Has a subject and a verb but starts with a subordinating conjunction (like *although, because, when, since*). It cannot stand alone. (e.g., *Because the dog barked.*)
- **Connecting Two Independent Clauses (IC + IC):**
    1.  **Period:** IC. IC.
    2.  **Semicolon:** IC; IC.
    3.  **Comma + FANBOYS (For, And, Nor, But, Or, Yet, So):** IC, and IC.
- **The Comma Splice Error:** You **CANNOT** join two independent clauses with just a comma. (e.g., *The dog barked, it was loud.* -> WRONG)
- **Connecting IC and DC:**
    1.  DC, IC. (Comma required: *Because it rained, we stayed inside.*)
    2.  IC DC. (Usually no comma: *We stayed inside because it rained.*)
- **Colons and Single Dashes:** Both a colon (:) and a single dash (-) are used to introduce an explanation, a list, or an example. **Rule:** You MUST have a complete, standalone Independent Clause *before* a colon or a single dash. What comes after can be a fragment, a list, or another IC.

## Worked Examples

**Example 1 (Comma Splice)**
*Passage:* The new art exhibit features over fifty contemporary sculptures from around the world _____ many critics have praised the curator for her bold selections.

*Question:* Which choice completes the text so that it conforms to the conventions of Standard English?
A) world,
B) world, and
C) world
D) world; and

*Step-by-step Reasoning:*
1. Analyze the first half: "The new art exhibit features over fifty contemporary sculptures from around the world." This is an Independent Clause (IC).
2. Analyze the second half: "many critics have praised the curator for her bold selections." This is also an Independent Clause (IC).
3. We have IC [blank] IC.
4. Evaluate choices:
    - (A) creates a comma splice (IC, IC). Incorrect.
    - (B) uses a comma + FANBOYS (IC, and IC). This is a correct way to link two ICs.
    - (C) creates a run-on sentence with no punctuation. Incorrect.
    - (D) uses a semicolon and FANBOYS. Semicolons act like periods. You don't use a semicolon *and* a FANBOYS together (IC; and IC is wrong).
5. Correct Answer: B.

**Example 2 (The Colon)**
*Passage:* During the expedition to the Amazon, the biologists discovered a remarkable new species of frog that possesses a unique defense mechanism _____ it can secrete a sticky, toxic resin from its skin when threatened.

*Question:* Which choice completes the text so that it conforms to the conventions of Standard English?
A) mechanism,
B) mechanism
C) mechanism:
D) mechanism, and

*Step-by-step Reasoning:*
1. Analyze the first half: "During the expedition... the biologists discovered a remarkable new species of frog that possesses a unique defense mechanism." This is an Independent Clause.
2. Analyze the second half: "it can secrete a sticky, toxic resin from its skin when threatened." This is also an Independent Clause. It acts as an explanation of the "defense mechanism."
3. Evaluate choices:
    - (A) creates a comma splice (IC, IC).
    - (B) creates a run-on sentence.
    - (D) "mechanism, and it can..." is grammatically acceptable (Comma + FANBOYS), but let's look at C.
    - (C) uses a colon. The rule for a colon is an IC before it, and an explanation after it. The second clause beautifully explains the "defense mechanism." The colon is elegant and correct here.
4. Correct Answer: C.

## Common Traps
1. **Conjunctive Adverbs:** Words like *however*, *therefore*, and *moreover* are NOT FANBOYS. You cannot use a comma before them to link two ICs. (e.g., *It rained, however, we played.* -> WRONG. Needs to be: *It rained; however, we played.*)
2. **Missing the Subject:** Sometimes the SAT uses a comma + FANBOYS, but the second half isn't an independent clause because it lacks a subject. (e.g., *He went to the store, and bought milk.* -> WRONG. No comma needed because "bought milk" isn't an IC. Should be: *He went to the store and bought milk.*)

## Quick Drills

**Question 1:**
*Passage:* The novel was an unexpected commercial success, selling millions of copies in its first month _____ the author, however, remained a recluse and refused to give any interviews.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) month,
B) month;
C) month
D) month, and

**Question 2:**
*Passage:* Researchers have discovered that the deep-sea anglerfish uses a bioluminescent lure to attract prey in the pitch-black environment of the ocean floor _____ a glowing bulb suspended from a rod-like appendage on its head.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) floor:
B) floor,
C) floor;
D) floor

**Question 3:**
*Passage:* Because the city council failed to allocate enough funds for public parks _____ the community center had to cancel its summer youth programs.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) parks;
B) parks,
C) parks
D) parks, and

**Answers:**
1. B (Semicolon separates two Independent Clauses. "however" is surrounded by commas inside the second clause).
2. A (Colon is used after an IC to introduce a description/appositive of the lure).
3. B (A Dependent Clause followed by an Independent Clause requires a comma).
"""
    },
    {
        'title': 'Standard English Conventions',
        'topic': 'Standard English Conventions',
        'subtopic': 'Standard English Conventions',
        'lecture_content': r"""# Standard English Conventions (Grammar & Punctuation)

## Overview
This module covers the "nitty-gritty" grammar rules tested on the SAT, primarily focusing on Subject-Verb Agreement, Verb Tense, Pronoun-Antecedent Agreement, and internal punctuation (like non-essential clauses and possessive apostrophes).

## Core Concepts
- **Subject-Verb Agreement:** Singular subjects take singular verbs (ends in -s: *The dog runs*). Plural subjects take plural verbs (no -s: *The dogs run*).
    - *The Prepositional Phrase Trap:* The SAT loves to put long prepositional phrases between the subject and the verb to confuse you. Cross them out!
    - Example: *The box [of chocolates] is empty.* (Not *are*).
- **Verb Tense:** Keep verbs consistent with the time frame of the sentence. Look for clue words (like *in 1999*, *currently*, *next year*).
- **Pronouns:** A pronoun must agree in number with the noun it replaces (its antecedent).
    - Singular nouns -> *it, its, he, his, she, her*
    - Plural nouns -> *they, them, their*
    - *Trick:* "Company," "team," and "government" are singular! (The team won *its* game, not *their* game).
- **Non-Essential Clauses:** Information that can be removed without ruining the grammatical structure of the sentence must be hugged by a pair of commas or a pair of dashes. You cannot mix and match a comma and a dash!
    - Correct: *My dog, a golden retriever, is asleep.*
    - Incorrect: *My dog, a golden retriever- is asleep.*
- **Apostrophes:** Used for possession or contractions.
    - Contraction: *It's* = It is. *They're* = They are.
    - Possession (Singular): *The boy's dog* (one boy).
    - Possession (Plural): *The boys' dog* (multiple boys).
    - *Its* is possessive. *It's* is "it is".

## Worked Examples

**Example 1 (Subject-Verb Agreement)**
*Passage:* The intricate patterns of the newly discovered butterfly species, which vary wildly depending on the temperature of the insect's habitat during the pupal stage, _____ fascinated entomologists around the world.

*Question:* Which choice completes the text so that it conforms to the conventions of Standard English?
A) has
B) have
C) is having
D) was having

*Step-by-step Reasoning:*
1. Find the verb options: *has, have, is, was*. We are dealing with verbs.
2. Find the subject. Who or what is doing the action? Cross out the prepositional phrases and non-essential clauses.
3. Sentence stripped down: "The intricate patterns [of the newly discovered butterfly species], [which vary wildly... stage], _____ fascinated entomologists..."
4. The core subject is "patterns." "Patterns" is plural.
5. Plural subjects require a plural verb.
6. Evaluate choices: (A) *has* is singular. (C) *is* is singular. (D) *was* is singular. (B) *have* is plural.
7. Correct Answer: B.

**Example 2 (Non-Essential Clause)**
*Passage:* Marie Curie _____ the first woman to win a Nobel Prize, remains one of the most iconic figures in the history of science.

*Question:* Which choice completes the text so that it conforms to the conventions of Standard English?
A) —who was
B) , who was
C) who was
D) , who was,

*Step-by-step Reasoning:*
1. The phrase "who was the first woman to win a Nobel Prize" is extra information describing Marie Curie. The core sentence is "Marie Curie remains one of the most iconic figures..."
2. Because it is extra (non-essential), it must be set off by matching punctuation.
3. Look at the end of the phrase: there is a comma after "Prize,".
4. Therefore, we need a comma at the beginning of the phrase to create a matching pair.
5. Evaluate choices: (A) uses a dash (mismatched with the comma later). (C) has no punctuation. (D) puts a comma after "was" which breaks the flow. (B) provides the opening comma.
6. Correct Answer: B.

## Common Traps
1. **Misidentifying the Subject:** Finding the noun closest to the verb and matching them, even though that noun is part of a prepositional phrase (e.g., *The flock of birds are flying* -> WRONG. *Flock* is singular, so it should be *is flying*).
2. **They're vs Their vs There:** 
    - *They're* = They are.
    - *Their* = Possessive (their coats).
    - *There* = Location (over there).
3. **Its vs It's:** Remembering that *its* (no apostrophe) is the possessive form, which defies the normal apostrophe rule for nouns.

## Quick Drills

**Question 1:**
*Passage:* A comprehensive study on the effects of urban noise pollution on local bird populations _____ recently published in a major scientific journal.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) were
B) are
C) was
D) have been

**Question 2:**
*Passage:* The startup company ultimately failed because it could not secure enough funding to support _____ ambitious expansion plans.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) they're
B) their
C) its
D) it's

**Question 3:**
*Passage:* George Washington Carver - a brilliant agricultural scientist who promoted alternative crops to cotton _____ developed hundreds of products using peanuts.

*Which choice completes the text so that it conforms to the conventions of Standard English?*
A) ,
B) ;
C) -
D) and

**Answers:**
1. C (The subject is "study", which is singular. "was" is the only singular verb).
2. C (The antecedent is "startup company", which is singular. The possessive singular pronoun is "its").
3. C (The non-essential clause starts with a dash, so it must end with a dash).
"""
    }
]

def seed_database():
    print("Starting database seed...")
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Seed Course
        cursor.execute('''
            INSERT OR REPLACE INTO courses (id, title, section, description)
            VALUES (?, ?, ?, ?)
        ''', (course['id'], course['title'], course['section'], course['description']))
        print(f"Seeded course: {course['title']}")
        
        # Seed Modules
        for i, mod in enumerate(modules):
            mod_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT OR REPLACE INTO course_modules (id, course_id, title, topic, subtopic, lecture_content, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (mod_id, course['id'], mod['title'], mod['topic'], mod['subtopic'], mod['lecture_content'], i+1))
            print(f"Seeded module {i+1}: {mod['title']} ({mod['topic']} | {mod['subtopic']})")

        conn.commit()
    print("Seed complete!")

if __name__ == '__main__':
    seed_database()
