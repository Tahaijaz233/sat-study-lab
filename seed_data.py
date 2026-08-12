import sqlite3
import datetime
import uuid
import hashlib
import json
from app.database import get_db

SEED_VOCAB = [
    {
        "word": "Ambiguous",
        "definition": "Open to more than one interpretation; having a double meaning.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "ambi- (both)",
        "synonyms": ["Equivocal", "Unclear", "Vague"],
        "antonyms": ["Clear", "Explicit", "Unambiguous"],
        "usage_examples": ["The ending of the movie was intentionally ambiguous.", "His ambiguous answer left us more confused than before."],
        "sentence_completion_drill": ["Because the instructions were _____, many students failed the assignment."]
    },
    {
        "word": "Pragmatic",
        "definition": "Dealing with things sensibly and realistically in a way that is based on practical rather than theoretical considerations.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "pragma- (deed, act)",
        "synonyms": ["Practical", "Realistic", "Sensible"],
        "antonyms": ["Idealistic", "Impractical", "Theoretical"],
        "usage_examples": ["She took a pragmatic approach to solving the problem.", "We need a pragmatic solution, not just a theoretical one."],
        "sentence_completion_drill": ["Rather than dreaming of a perfect world, the politician offered _____ solutions to everyday problems."]
    },
    {
        "word": "Bolster",
        "definition": "Support or strengthen; prop up.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "N/A",
        "synonyms": ["Reinforce", "Strengthen", "Boost"],
        "antonyms": ["Undermine", "Weaken", "Hinder"],
        "usage_examples": ["The fall in interest rates is starting to bolster confidence.", "She used extra examples to bolster her argument."],
        "sentence_completion_drill": ["The sudden influx of donations helped to _____ the charity's struggling programs."]
    },
    {
        "word": "Undermine",
        "definition": "Damage or weaken (someone or something), especially gradually or insidiously.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "under- (below)",
        "synonyms": ["Sabotage", "Subvert", "Weaken"],
        "antonyms": ["Bolster", "Support", "Enhance"],
        "usage_examples": ["This could undermine years of hard work.", "The constant criticism began to undermine her confidence."],
        "sentence_completion_drill": ["The frequent interruptions served only to _____ the speaker's authority."]
    },
    {
        "word": "Anomalous",
        "definition": "Deviating from what is standard, normal, or expected.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "an- (not) + homos (same)",
        "synonyms": ["Abnormal", "Atypical", "Irregular"],
        "antonyms": ["Normal", "Standard", "Typical"],
        "usage_examples": ["The researchers noted an anomalous result in the experiment.", "His anomalous behavior worried his friends."],
        "sentence_completion_drill": ["The snowstorm in July was a highly _____ event for the region."]
    },
    {
        "word": "Equivocal",
        "definition": "Open to more than one interpretation; ambiguous.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "equi- (equal) + voc- (voice)",
        "synonyms": ["Ambiguous", "Noncommittal", "Vague"],
        "antonyms": ["Certain", "Clear", "Unequivocal"],
        "usage_examples": ["The politician gave an equivocal answer to the reporter's question.", "The evidence was equivocal, leaving the jury unsure."],
        "sentence_completion_drill": ["Her _____ response made it difficult to tell if she supported the plan or not."]
    },
    {
        "word": "Ubiquitous",
        "definition": "Present, appearing, or found everywhere.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "ubi- (where)",
        "synonyms": ["Omnipresent", "Pervasive", "Universal"],
        "antonyms": ["Rare", "Scarce", "Uncommon"],
        "usage_examples": ["Smartphones have become ubiquitous in modern society.", "The company's logo is ubiquitous, seen on billboards everywhere."],
        "sentence_completion_drill": ["Coffee shops are so _____ in this city that you can find one on nearly every corner."]
    },
    {
        "word": "Ephemeral",
        "definition": "Lasting for a very short time.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "eph- (upon) + hemera (day)",
        "synonyms": ["Fleeting", "Transient", "Short-lived"],
        "antonyms": ["Permanent", "Enduring", "Everlasting"],
        "usage_examples": ["Fashions are ephemeral, changing with every season.", "The beauty of the sunset was ephemeral."],
        "sentence_completion_drill": ["The fame of internet celebrities is often _____, lasting only until the next trend emerges."]
    },
    {
        "word": "Empirical",
        "definition": "Based on, concerned with, or verifiable by observation or experience rather than theory or pure logic.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "em- (in) + peira (trial)",
        "synonyms": ["Observational", "Practical", "Factual"],
        "antonyms": ["Theoretical", "Hypothetical", "Conjectural"],
        "usage_examples": ["They provided considerable empirical evidence to support their claims.", "The theory needs to be backed up with empirical data."],
        "sentence_completion_drill": ["The scientist refused to accept the hypothesis without _____ evidence to support it."]
    },
    {
        "word": "Explicit",
        "definition": "Stated clearly and in detail, leaving no room for confusion or doubt.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "ex- (out) + plicare (to fold)",
        "synonyms": ["Clear", "Direct", "Specific"],
        "antonyms": ["Implicit", "Vague", "Ambiguous"],
        "usage_examples": ["The instructions were explicit and easy to follow.", "He gave explicit orders that he was not to be disturbed."],
        "sentence_completion_drill": ["Because her directions were _____, we found the hidden cabin with no trouble."]
    },
    {
        "word": "Implicit",
        "definition": "Implied though not plainly expressed.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "im- (in) + plicare (to fold)",
        "synonyms": ["Implied", "Inferred", "Understood"],
        "antonyms": ["Explicit", "Stated", "Direct"],
        "usage_examples": ["There was an implicit agreement that he would pay for dinner.", "Her words contained an implicit threat."],
        "sentence_completion_drill": ["Although it was never formalized, an _____ understanding existed between the two rivals."]
    },
    {
        "word": "Comprehensive",
        "definition": "Complete; including all or nearly all elements or aspects of something.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "com- (together) + prehendere (to grasp)",
        "synonyms": ["Thorough", "Complete", "Extensive"],
        "antonyms": ["Limited", "Partial", "Incomplete"],
        "usage_examples": ["The report provided a comprehensive overview of the issue.", "She has a comprehensive knowledge of the subject."],
        "sentence_completion_drill": ["The insurance policy is _____, covering everything from theft to natural disasters."]
    },
    {
        "word": "Superfluous",
        "definition": "Unnecessary, especially through being more than enough.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "super- (over) + fluere (to flow)",
        "synonyms": ["Redundant", "Excess", "Unneeded"],
        "antonyms": ["Essential", "Necessary", "Vital"],
        "usage_examples": ["The purchaser should avoid asking for superfluous information.", "My presence at the meeting seemed superfluous."],
        "sentence_completion_drill": ["Because the manual was already detailed, the extra appendix seemed entirely _____."]
    },
    {
        "word": "Paradoxical",
        "definition": "Seemingly absurd or self-contradictory.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "para- (contrary to) + doxa (opinion)",
        "synonyms": ["Contradictory", "Incongruous", "Illogical"],
        "antonyms": ["Logical", "Consistent", "Expected"],
        "usage_examples": ["It is paradoxical that standing is more tiring than walking.", "The medication had a paradoxical effect, making him more energetic instead of sleepy."],
        "sentence_completion_drill": ["It was a _____ situation: the more she studied, the worse she performed on the tests."]
    },
    {
        "word": "Mitigate",
        "definition": "Make less severe, serious, or painful.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "mitis (mild) + agere (to do)",
        "synonyms": ["Alleviate", "Reduce", "Lessen"],
        "antonyms": ["Exacerbate", "Aggravate", "Intensify"],
        "usage_examples": ["The doctor prescribed medication to mitigate the pain.", "They planted trees to mitigate the effects of pollution."],
        "sentence_completion_drill": ["The government provided financial aid to _____ the devastating effects of the hurricane."]
    },
    {
        "word": "Exacerbate",
        "definition": "Make (a problem, bad situation, or negative feeling) worse.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "ex- (out of) + acerbus (harsh)",
        "synonyms": ["Aggravate", "Worsen", "Intensify"],
        "antonyms": ["Mitigate", "Alleviate", "Improve"],
        "usage_examples": ["His angry comments only served to exacerbate the situation.", "The new law could exacerbate the housing crisis."],
        "sentence_completion_drill": ["Scratching the mosquito bite will only _____ the itching."]
    },
    {
        "word": "Aesthetic",
        "definition": "Concerned with beauty or the appreciation of beauty.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "aisthanesthai (to perceive)",
        "synonyms": ["Artistic", "Beautiful", "Tasteful"],
        "antonyms": ["Ugly", "Unattractive", "Displeasing"],
        "usage_examples": ["The building has a great aesthetic appeal.", "She changed the font for aesthetic reasons."],
        "sentence_completion_drill": ["The director's _____ vision transformed the gritty script into a visually stunning film."]
    },
    {
        "word": "Disparate",
        "definition": "Essentially different in kind; not allowing comparison.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "dis- (apart) + parare (to prepare/equal)",
        "synonyms": ["Contrasting", "Different", "Diverse"],
        "antonyms": ["Homogeneous", "Similar", "Uniform"],
        "usage_examples": ["They inhabit disparate worlds of thought.", "The group is made up of individuals from wildly disparate backgrounds."],
        "sentence_completion_drill": ["The committee struggled to combine the _____ views of its members into a unified proposal."]
    },
    {
        "word": "Substantiate",
        "definition": "Provide evidence to support or prove the truth of.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "sub- (under) + stare (to stand)",
        "synonyms": ["Prove", "Verify", "Corroborate"],
        "antonyms": ["Disprove", "Refute", "Contradict"],
        "usage_examples": ["They had found nothing to substantiate the allegations.", "Please provide documentation to substantiate your claims."],
        "sentence_completion_drill": ["The detective needed more clues to _____ his theory about the robbery."]
    },
    {
        "word": "Refute",
        "definition": "Prove (a statement or theory) to be wrong or false; disprove.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "re- (back) + futare (to beat)",
        "synonyms": ["Disprove", "Debunk", "Contradict"],
        "antonyms": ["Confirm", "Substantiate", "Prove"],
        "usage_examples": ["These claims have not been convincingly refuted.", "She wrote an article attempting to refute the scientist's findings."],
        "sentence_completion_drill": ["The lawyer presented compelling evidence to _____ the prosecutor's argument."]
    },
    {
        "word": "Prevalent",
        "definition": "Widespread in a particular area at a particular time.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "pre- (before) + valere (to have power)",
        "synonyms": ["Widespread", "Common", "Frequent"],
        "antonyms": ["Rare", "Uncommon", "Unusual"],
        "usage_examples": ["The social ills prevalent in society today are complex.", "This disease is more prevalent among older people."],
        "sentence_completion_drill": ["Given how _____ the rumor was, it was surprising to find out it was entirely false."]
    },
    {
        "word": "Fastidious",
        "definition": "Very attentive to and concerned about accuracy and detail.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "fastidium (loathing)",
        "synonyms": ["Meticulous", "Punctilious", "Fussy"],
        "antonyms": ["Careless", "Sloppy", "Lax"],
        "usage_examples": ["He chooses his words with fastidious care.", "She is a fastidious cleaner."],
        "sentence_completion_drill": ["The _____ editor caught every single typo in the massive manuscript."]
    },
    {
        "word": "Tenacious",
        "definition": "Tending to keep a firm hold of something; clinging or adhering closely.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "tenere (to hold)",
        "synonyms": ["Persistent", "Stubborn", "Determined"],
        "antonyms": ["Yielding", "Weak", "Fickle"],
        "usage_examples": ["He has a tenacious grip on reality.", "She was tenacious in pursuit of her goals."],
        "sentence_completion_drill": ["Despite facing numerous setbacks, the _____ runner finished the marathon."]
    },
    {
        "word": "Esoteric",
        "definition": "Intended for or likely to be understood by only a small number of people with a specialized knowledge or interest.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "esotero (inner)",
        "synonyms": ["Obscure", "Arcane", "Cryptic"],
        "antonyms": ["Common", "Familiar", "Known"],
        "usage_examples": ["He has an esoteric collection of old texts.", "The philosophy seemed esoteric to the casual reader."],
        "sentence_completion_drill": ["The professor's lectures were so _____ that only his graduate students could follow along."]
    },
    {
        "word": "Meticulous",
        "definition": "Showing great attention to detail; very careful and precise.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "metus (fear)",
        "synonyms": ["Careful", "Conscientious", "Diligent"],
        "antonyms": ["Careless", "Sloppy", "Inexact"],
        "usage_examples": ["He had always been so meticulous about his appearance.", "The research required meticulous planning."],
        "sentence_completion_drill": ["Building a model ship inside a bottle requires a _____ touch."]
    },
    {
        "word": "Plausible",
        "definition": "(of an argument or statement) seeming reasonable or probable.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "plaudere (to applaud)",
        "synonyms": ["Credible", "Reasonable", "Believable"],
        "antonyms": ["Implausible", "Unlikely", "Impossible"],
        "usage_examples": ["She gave a plausible explanation for her lateness.", "It is a plausible theory, but it needs to be tested."],
        "sentence_completion_drill": ["The suspect's alibi seemed _____ at first, but further investigation revealed inconsistencies."]
    },
    {
        "word": "Elucidate",
        "definition": "Make (something) clear; explain.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "e- (out) + lucidus (lucid, bright)",
        "synonyms": ["Explain", "Clarify", "Illuminate"],
        "antonyms": ["Confuse", "Obscure", "Complicate"],
        "usage_examples": ["Please elucidate the reasons for your decision.", "The notes helped to elucidate the difficult text."],
        "sentence_completion_drill": ["The diagrams in the textbook helped to _____ the complex biological process."]
    },
    {
        "word": "Proponent",
        "definition": "A person who advocates a theory, proposal, or project.",
        "part_of_speech": "Noun",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "pro- (forward) + ponere (to put)",
        "synonyms": ["Advocate", "Supporter", "Champion"],
        "antonyms": ["Opponent", "Critic", "Detractor"],
        "usage_examples": ["He is a strong proponent of renewable energy.", "The proponents of the bill argued it would save money."],
        "sentence_completion_drill": ["As a _____ of healthy eating, she campaigned to have vending machines removed from schools."]
    },
    {
        "word": "Adversary",
        "definition": "One's opponent in a contest, conflict, or dispute.",
        "part_of_speech": "Noun",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "ad- (to) + vertere (to turn)",
        "synonyms": ["Opponent", "Rival", "Enemy"],
        "antonyms": ["Ally", "Friend", "Supporter"],
        "usage_examples": ["He saw her as his main adversary within the company.", "The two teams have been adversaries for decades."],
        "sentence_completion_drill": ["In the final match of the tournament, he faced his long-time _____."]
    },
    {
        "word": "Synthesize",
        "definition": "Make (something) by synthesis, especially chemically; combine (a number of things) into a coherent whole.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "syn- (together) + tithenai (to place)",
        "synonyms": ["Combine", "Blend", "Integrate"],
        "antonyms": ["Separate", "Divide", "Analyze"],
        "usage_examples": ["Darwin synthesized ideas from many different fields.", "The students were asked to synthesize information from three different sources."],
        "sentence_completion_drill": ["To write a successful essay, you must _____ evidence from multiple articles to support your thesis."]
    },
    {
        "word": "Nuance",
        "definition": "A subtle difference in or shade of meaning, expression, or sound.",
        "part_of_speech": "Noun",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "nubes (cloud)",
        "synonyms": ["Subtlety", "Distinction", "Gradation"],
        "antonyms": ["Obviousness", "Bluntness", "Simplicity"],
        "usage_examples": ["He understood the nuances of the language.", "The actor's performance lacked nuance."],
        "sentence_completion_drill": ["Translating poetry is difficult because capturing every _____ of the original language is nearly impossible."]
    },
    {
        "word": "Assert",
        "definition": "State a fact or belief confidently and forcefully.",
        "part_of_speech": "Verb",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "ad- (to) + serere (to join)",
        "synonyms": ["Declare", "Maintain", "Contend"],
        "antonyms": ["Deny", "Reject", "Retract"],
        "usage_examples": ["The company asserts that the cuts will not affect service.", "He asserted his innocence from the beginning."],
        "sentence_completion_drill": ["Despite the lack of evidence, the witness continued to _____ that she had seen a UFO."]
    },
    {
        "word": "Concede",
        "definition": "Admit that something is true or valid after first denying or resisting it.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "con- (completely) + cedere (to yield)",
        "synonyms": ["Admit", "Acknowledge", "Accept"],
        "antonyms": ["Deny", "Dispute", "Reject"],
        "usage_examples": ["I had to concede that I'd overreacted.", "He finally conceded defeat in the election."],
        "sentence_completion_drill": ["After hours of debate, the debater was forced to _____ that her opponent had made a valid point."]
    },
    {
        "word": "Invariably",
        "definition": "In every case or on every occasion; always.",
        "part_of_speech": "Adverb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "in- (not) + varius (changing)",
        "synonyms": ["Always", "Consistently", "Unfailingly"],
        "antonyms": ["Rarely", "Sometimes", "Never"],
        "usage_examples": ["The meals here are invariably excellent.", "He invariably arrives late for meetings."],
        "sentence_completion_drill": ["Whenever they try to fix the old car, they _____ end up breaking something else."]
    },
    {
        "word": "Evoke",
        "definition": "Bring or recall to the conscious mind.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "e- (out) + vocare (to call)",
        "synonyms": ["Elicit", "Summon", "Provoke"],
        "antonyms": ["Suppress", "Halt", "Stifle"],
        "usage_examples": ["The sight of asterisks evokes memories of early computing.", "The music evoked a sense of profound sadness."],
        "sentence_completion_drill": ["The old photograph managed to _____ powerful feelings of nostalgia in the elderly woman."]
    },
    {
        "word": "Incisive",
        "definition": "(of a person or mental process) intelligently analytical and clear-thinking.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "in- (into) + caedere (to cut)",
        "synonyms": ["Penetrating", "Acute", "Sharp"],
        "antonyms": ["Vague", "Dull", "Rambling"],
        "usage_examples": ["She was an incisive critic.", "His incisive questioning revealed the flaws in the plan."],
        "sentence_completion_drill": ["The journalist's _____ questions quickly got to the heart of the scandal."]
    },
    {
        "word": "Intricate",
        "definition": "Very complicated or detailed.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "in- (into) + tricae (perplexities)",
        "synonyms": ["Complex", "Complicated", "Elaborate"],
        "antonyms": ["Simple", "Straightforward", "Basic"],
        "usage_examples": ["The intricate patterns on the carpet were mesmerizing.", "An intricate network of canals crisscrossed the city."],
        "sentence_completion_drill": ["The plot of the mystery novel was so _____ that readers had to pay close attention to every detail."]
    },
    {
        "word": "Scrutinize",
        "definition": "Examine or inspect closely and thoroughly.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "scrutari (to search)",
        "synonyms": ["Examine", "Inspect", "Analyze"],
        "antonyms": ["Ignore", "Glance at", "Overlook"],
        "usage_examples": ["Customers were warned to scrutinize the small print.", "The accountant scrutinized the company's financial records."],
        "sentence_completion_drill": ["The art expert began to _____ the painting, looking for signs of forgery."]
    },
    {
        "word": "Perceptive",
        "definition": "Having or showing sensitive insight.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "percipere (to grasp)",
        "synonyms": ["Insightful", "Observant", "Astute"],
        "antonyms": ["Oblivious", "Unobservant", "Dense"],
        "usage_examples": ["It was very perceptive of you to notice that.", "He was a perceptive observer of human nature."],
        "sentence_completion_drill": ["The _____ teacher quickly realized that the student was struggling with issues at home."]
    },
    {
        "word": "Disseminate",
        "definition": "Spread (something, especially information) widely.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "dis- (apart) + semen (seed)",
        "synonyms": ["Spread", "Circulate", "Distribute"],
        "antonyms": ["Conceal", "Hide", "Suppress"],
        "usage_examples": ["Health authorities should foster good practice by disseminating information.", "The internet makes it easy to disseminate news rapidly."],
        "sentence_completion_drill": ["The main goal of the organization is to _____ information about climate change to the public."]
    },
    {
        "word": "Alleviate",
        "definition": "Make (suffering, deficiency, or a problem) less severe.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "ad- (to) + levis (light)",
        "synonyms": ["Reduce", "Relieve", "Ease"],
        "antonyms": ["Aggravate", "Exacerbate", "Worsen"],
        "usage_examples": ["He couldn't prevent her pain, only alleviate it.", "Measures were taken to alleviate the traffic congestion."],
        "sentence_completion_drill": ["Applying ice to the sprained ankle helped to _____ the swelling and pain."]
    },
    {
        "word": "Concur",
        "definition": "Be of the same opinion; agree.",
        "part_of_speech": "Verb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "con- (together) + currere (to run)",
        "synonyms": ["Agree", "Assent", "Coincide"],
        "antonyms": ["Disagree", "Clash", "Differ"],
        "usage_examples": ["The authors concurred with the majority view.", "I strongly concur with your assessment of the situation."],
        "sentence_completion_drill": ["Although they often argued, the siblings did _____ that their family vacations were always fun."]
    },
    {
        "word": "Discrepancy",
        "definition": "An illogical or surprising lack of compatibility or similarity between two or more facts.",
        "part_of_speech": "Noun",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "dis- (apart) + crepare (to sound)",
        "synonyms": ["Inconsistency", "Difference", "Disparity"],
        "antonyms": ["Agreement", "Similarity", "Consistency"],
        "usage_examples": ["There's a discrepancy between your account and his.", "The auditors found a large discrepancy in the financial records."],
        "sentence_completion_drill": ["The _____ between the witness's statement and the video footage raised suspicions."]
    },
    {
        "word": "Subjective",
        "definition": "Based on or influenced by personal feelings, tastes, or opinions.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "sub- (under) + jacere (to throw)",
        "synonyms": ["Personal", "Biased", "Individual"],
        "antonyms": ["Objective", "Impartial", "Unbiased"],
        "usage_examples": ["His views are highly subjective.", "Art appreciation is inherently subjective."],
        "sentence_completion_drill": ["Grading essays can be difficult because the evaluation is somewhat _____."]
    },
    {
        "word": "Objective",
        "definition": "(of a person or their judgment) not influenced by personal feelings or opinions in considering and representing facts.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "ob- (against) + jacere (to throw)",
        "synonyms": ["Impartial", "Unbiased", "Neutral"],
        "antonyms": ["Subjective", "Biased", "Partial"],
        "usage_examples": ["Historians try to be objective and impartial.", "We need an objective assessment of the situation."],
        "sentence_completion_drill": ["A judge must remain _____ when hearing a case, putting aside all personal prejudices."]
    },
    {
        "word": "Benchmark",
        "definition": "A standard or point of reference against which things may be compared or assessed.",
        "part_of_speech": "Noun",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "N/A",
        "synonyms": ["Standard", "Reference", "Yardstick"],
        "antonyms": ["Outlier", "Anomaly", "Exception"],
        "usage_examples": ["The settlement became a new benchmark for compensation levels.", "This test is used as a benchmark for student performance."],
        "sentence_completion_drill": ["The company's excellent customer service has become the _____ for the entire industry."]
    },
    {
        "word": "Feasible",
        "definition": "Possible to do easily or conveniently.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "facere (to do, make)",
        "synonyms": ["Possible", "Practical", "Viable"],
        "antonyms": ["Impossible", "Impractical", "Unfeasible"],
        "usage_examples": ["It is not feasible to put most finds from excavations on public display.", "The plan seemed feasible at first, but costs soon escalated."],
        "sentence_completion_drill": ["Before starting construction, the city council commissioned a study to see if the new bridge was _____."]
    },
    {
        "word": "Precursor",
        "definition": "A person or thing that comes before another of the same kind; a forerunner.",
        "part_of_speech": "Noun",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "pre- (before) + currere (to run)",
        "synonyms": ["Forerunner", "Predecessor", "Antecedent"],
        "antonyms": ["Successor", "Descendant", "Result"],
        "usage_examples": ["A three-stringed violoncello was the precursor of the modern violin.", "High blood pressure is often a precursor to heart disease."],
        "sentence_completion_drill": ["The invention of the telegraph served as a _____ to the telephone."]
    },
    {
        "word": "Inadvertently",
        "definition": "Without intention; accidentally.",
        "part_of_speech": "Adverb",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "in- (not) + advertere (to turn toward)",
        "synonyms": ["Accidentally", "Unintentionally", "Unwittingly"],
        "antonyms": ["Deliberately", "Intentionally", "Purposefully"],
        "usage_examples": ["His name had been inadvertently omitted from the list.", "I inadvertently deleted the important file."],
        "sentence_completion_drill": ["While trying to clean her keyboard, she _____ sent an incomplete email to her boss."]
    },
    {
        "word": "Candid",
        "definition": "Truthful and straightforward; frank.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "candidus (white)",
        "synonyms": ["Frank", "Honest", "Direct"],
        "antonyms": ["Deceitful", "Evasive", "Insincere"],
        "usage_examples": ["His responses were remarkably candid.", "I appreciate your candid feedback."],
        "sentence_completion_drill": ["The documentary offered a _____ look at the daily struggles of healthcare workers."]
    },
    {
        "word": "Enigmatic",
        "definition": "Difficult to interpret or understand; mysterious.",
        "part_of_speech": "Adjective",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "ainigma (riddle)",
        "synonyms": ["Mysterious", "Puzzling", "Baffling"],
        "antonyms": ["Clear", "Obvious", "Straightforward"],
        "usage_examples": ["He took the money with an enigmatic smile.", "The Mona Lisa is famous for her enigmatic expression."],
        "sentence_completion_drill": ["The author's latest novel features an _____ protagonist whose motives remain unclear until the final page."]
    },
    {
        "word": "Diligent",
        "definition": "Having or showing care and conscientiousness in one's work or duties.",
        "part_of_speech": "Adjective",
        "difficulty": "Easy",
        "roots_prefixes_suffixes": "dis- (apart) + legere (to choose)",
        "synonyms": ["Industrious", "Hard-working", "Assiduous"],
        "antonyms": ["Lazy", "Negligent", "Careless"],
        "usage_examples": ["Many caves are located only after a diligent search.", "She was a diligent student who always finished her assignments early."],
        "sentence_completion_drill": ["The _____ researcher spent months combing through the archives for evidence."]
    },
    {
        "word": "Novel",
        "definition": "New or unusual in an interesting way.",
        "part_of_speech": "Adjective",
        "difficulty": "Medium",
        "roots_prefixes_suffixes": "novus (new)",
        "synonyms": ["New", "Original", "Innovative"],
        "antonyms": ["Old", "Conventional", "Familiar"],
        "usage_examples": ["He hit on a novel idea to solve his financial problems.", "The company introduced a novel approach to recycling."],
        "sentence_completion_drill": ["Instead of a traditional lecture, the professor used a _____ teaching method that involved interactive games."]
    },
    {
        "word": "Vindicate",
        "definition": "Clear (someone) of blame or suspicion.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "vim dicare (to show authority)",
        "synonyms": ["Exonerate", "Clear", "Absolve"],
        "antonyms": ["Condemn", "Blame", "Convict"],
        "usage_examples": ["Hospital staff were vindicated by the inquest verdict.", "The new evidence will vindicate my client completely."],
        "sentence_completion_drill": ["After years in prison, the DNA evidence finally served to _____ the wrongfully accused man."]
    },
    {
        "word": "Exonerate",
        "definition": "(especially of an official body) absolve (someone) from blame for a fault or wrongdoing, especially after due consideration of the case.",
        "part_of_speech": "Verb",
        "difficulty": "Hard",
        "roots_prefixes_suffixes": "ex- (from) + onus (burden)",
        "synonyms": ["Absolve", "Clear", "Acquit"],
        "antonyms": ["Convict", "Condemn", "Blame"],
        "usage_examples": ["The court-martial exonerated me.", "An independent investigation exonerated the mayor of any wrongdoing."],
        "sentence_completion_drill": ["The security footage was enough to _____ the employee, proving he was not near the cash register at the time of the theft."]
    }
]

SEED_SOURCES = [
    {
        "id": "src_sat_lab_orig",
        "name": "SAT Study Lab Original",
        "uri": "https://satstudylab.org/original-content",
        "source_type": "Official Public Domain / Licensed",
        "permission_notes": "Original questions and vocab created for SAT Study Lab under CC BY 4.0."
    }
]

SEED_QUESTIONS = [
    {
        "section": "Reading and Writing",
        "topic": "Information and Ideas",
        "subtopic": "Central Ideas and Details",
        "difficulty": "Medium",
        "passage_text": "In recent decades, historians have increasingly recognized the role of weather patterns in shaping historical events. While past scholars often attributed the fall of the Ming Dynasty in 1644 solely to economic mismanagement and internal rebellion, modern researchers point to severe droughts and cold temperatures during this period. These conditions devastated crop yields, leading to widespread famine and unrest, which fatally weakened the dynasty's ability to govern.",
        "prompt": "Which statement best summarizes the main idea of the text?",
        "choices": [
            "The Ming Dynasty fell primarily because of poor economic decisions made by its leaders.",
            "Modern historians believe that the Ming Dynasty's fall was inevitable due to internal rebellions.",
            "Weather conditions played a significant, previously underappreciated role in the collapse of the Ming Dynasty.",
            "Historians disagree on the exact year the Ming Dynasty lost its power due to conflicting records."
        ],
        "correct_answer_value": "C",
        "explanation": "The text states that historians increasingly recognize the role of weather in historical events, specifically noting that modern researchers point to severe droughts and cold temperatures as significant factors in the fall of the Ming Dynasty.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Reading and Writing",
        "topic": "Craft and Structure",
        "subtopic": "Words in Context",
        "difficulty": "Easy",
        "passage_text": "Despite her extensive preparation and deep knowledge of the subject matter, Maria found the debate to be unexpectedly challenging. Her opponent's arguments were not only well-researched but also delivered with a level of confidence that left Maria feeling ______.",
        "prompt": "Which choice completes the text with the most logical and precise word or phrase?",
        "choices": [
            "invigorated",
            "unsettled",
            "indifferent",
            "triumphant"
        ],
        "correct_answer_value": "B",
        "explanation": "The text indicates the debate was unexpectedly challenging for Maria because of her opponent's strong arguments and confidence. This would likely leave her feeling 'unsettled'.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Reading and Writing",
        "topic": "Expression of Ideas",
        "subtopic": "Transitions",
        "difficulty": "Medium",
        "passage_text": "Solar panels provide a clean and renewable source of energy, and many homeowners install them to reduce their electricity bills. ______, the initial cost of purchasing and installing a solar panel system can be prohibitively expensive for some families.",
        "prompt": "Which choice completes the text with the most logical transition?",
        "choices": [
            "Consequently",
            "In addition",
            "However",
            "For example"
        ],
        "correct_answer_value": "C",
        "explanation": "The first sentence discusses benefits, while the second sentence discusses a drawback. 'However' is the correct transition showing contrast.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Reading and Writing",
        "topic": "Standard English Conventions",
        "subtopic": "Boundaries",
        "difficulty": "Hard",
        "passage_text": "The recently discovered exoplanet Kepler-186f is approximately 500 light-years away from Earth. Because it orbits within its star's habitable zone, where liquid water could exist on the ______ scientists are eager to study its atmosphere for signs of life.",
        "prompt": "Which choice completes the text so that it conforms to the conventions of Standard English?",
        "choices": [
            "surface:",
            "surface;",
            "surface,",
            "surface"
        ],
        "correct_answer_value": "C",
        "explanation": "The clause beginning with 'Because...' is a dependent clause that introduces the main independent clause. A comma is required.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Reading and Writing",
        "topic": "Information and Ideas",
        "subtopic": "Command of Evidence",
        "difficulty": "Hard",
        "passage_text": "To determine whether physical exercise improves cognitive function in older adults, a research team conducted a six-month study. Group A participated in aerobic exercises three times a week, while Group B engaged in stretching and toning exercises. At the end of the study, Group A showed significant improvements in memory recall tests compared to Group B. The researchers concluded that aerobic exercise specifically enhances memory in older adults.",
        "prompt": "Which finding, if true, would most directly weaken the researchers' conclusion?",
        "choices": [
            "Group B showed improvements in flexibility and balance that Group A did not.",
            "Group A was given a dietary supplement known to enhance memory throughout the duration of the study.",
            "Participants in Group A reported feeling more energetic after the aerobic sessions.",
            "The memory recall tests used at the beginning and end of the study were identical."
        ],
        "correct_answer_value": "B",
        "explanation": "If Group A also took a memory-enhancing supplement, it introduces an alternative cause for the improvement, weakening the conclusion about aerobic exercise.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Math",
        "topic": "Algebra",
        "subtopic": "Linear Equations",
        "difficulty": "Easy",
        "passage_text": "",
        "prompt": "If $3x - 5 = 16$, what is the value of $x$?",
        "choices": [
            "5",
            "7",
            "11",
            "21"
        ],
        "correct_answer_value": "B",
        "explanation": "Add 5 to both sides: $3x = 21$. Then divide by 3: $x = 7$.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Math",
        "topic": "Advanced Math",
        "subtopic": "Quadratic Equations",
        "difficulty": "Medium",
        "passage_text": "",
        "prompt": "Which of the following represents the solutions to the equation $x^2 - 6x + 8 = 0$?",
        "choices": [
            "$x = 2$ and $x = 4$",
            "$x = -2$ and $x = -4$",
            "$x = 1$ and $x = 8$",
            "$x = -1$ and $x = -8$"
        ],
        "correct_answer_value": "A",
        "explanation": "The quadratic factors as $(x - 2)(x - 4) = 0$, giving $x = 2$ and $x = 4$.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Math",
        "topic": "Problem Solving and Data Analysis",
        "subtopic": "Percentages",
        "difficulty": "Medium",
        "passage_text": "",
        "prompt": r"A store is having a sale where all items are discounted by 20%. If the sale price of a jacket is $\$64$, what was its original price in dollars?",
        "choices": [
            "72",
            "80",
            "84",
            "100"
        ],
        "correct_answer_value": "B",
        "explanation": r"$0.80P = 64 \implies P = 64 / 0.80 = 80$.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Math",
        "topic": "Advanced Math",
        "subtopic": "Exponents",
        "difficulty": "Hard",
        "passage_text": "",
        "prompt": r"If $2^{3x} = 64$, what is the value of $x$?",
        "choices": [], 
        "correct_answer_value": "2",
        "explanation": r"$64 = 2^6 \implies 2^{3x} = 2^6 \implies 3x = 6 \implies x = 2$.",
        "source_name": "SAT Study Lab Original"
    },
    {
        "section": "Math",
        "topic": "Geometry and Trigonometry",
        "subtopic": "Circles",
        "difficulty": "Hard",
        "passage_text": "",
        "prompt": "The equation of a circle in the $xy$-plane is $x^2 + y^2 - 4x + 6y = 12$. What is the radius of the circle?",
        "choices": [],
        "correct_answer_value": "5",
        "explanation": "Complete the square: $(x - 2)^2 + (y + 3)^2 = 12 + 4 + 9 = 25$. Radius $r = \\sqrt{25} = 5$.",
        "source_name": "SAT Study Lab Original"
    }
]

def seed_all():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Sources
        source_map = {}
        for src in SEED_SOURCES:
            cursor.execute('''
                INSERT OR IGNORE INTO sources (id, name, uri, source_type, permission_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (src['id'], src['name'], src.get('uri'), src['source_type'], src.get('permission_notes')))
            source_map[src['name']] = src['id']

        # 2. Vocabulary (55 terms)
        today = datetime.date.today().isoformat()
        vocab_inserted = 0
        for word_data in SEED_VOCAB:
            cursor.execute('SELECT id FROM vocab_terms WHERE word = ?', (word_data['word'],))
            if not cursor.fetchone():
                vocab_id = f"vocab_{uuid.uuid4().hex[:10]}"
                cursor.execute('''
                    INSERT INTO vocab_terms (
                        id, word, definition, part_of_speech, difficulty,
                        roots_prefixes_suffixes, synonyms, antonyms,
                        usage_examples, sentence_completion_drill,
                        status, repetition_interval, repetition_efactor, repetition_count,
                        next_review_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vocab_id,
                    word_data['word'],
                    word_data['definition'],
                    word_data.get('part_of_speech'),
                    word_data.get('difficulty'),
                    word_data.get('roots_prefixes_suffixes'),
                    json.dumps(word_data.get('synonyms', [])),
                    json.dumps(word_data.get('antonyms', [])),
                    json.dumps(word_data.get('usage_examples', [])),
                    json.dumps(word_data.get('sentence_completion_drill', [])),
                    'unseen', 1, 2.5, 0, today
                ))
                vocab_inserted += 1

        # 3. Passages & Questions
        qs_inserted = 0
        for q in SEED_QUESTIONS:
            content_hash = hashlib.sha256((q['prompt'] + (q.get('passage_text') or '')).encode('utf-8')).hexdigest()
            
            cursor.execute('SELECT id FROM questions WHERE content_hash = ?', (content_hash,))
            if cursor.fetchone():
                continue
                
            passage_id = None
            if q.get('passage_text'):
                passage_id = f"pas_{uuid.uuid4().hex[:10]}"
                cursor.execute('''
                    INSERT INTO passages (id, title, content, passage_type, word_count, source_name)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (passage_id, f"Passage - {q['topic']}", q['passage_text'], 'Reading', len(q['passage_text'].split()), q['source_name']))

            q_id = f"q_{uuid.uuid4().hex[:10]}"
            is_spr = len(q.get('choices', [])) == 0
            q_type = "Student-Produced Response" if is_spr else "Multiple Choice"

            cursor.execute('''
                INSERT INTO questions (
                    id, passage_id, section, topic, subtopic, question_type,
                    difficulty, prompt, answer_explanation, correct_answer_value,
                    source_name, content_hash
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                q_id, passage_id, q['section'], q['topic'], q['subtopic'], q_type,
                q['difficulty'], q['prompt'], q['explanation'], q['correct_answer_value'],
                q['source_name'], content_hash
            ))

            if not is_spr:
                letters = ['A', 'B', 'C', 'D']
                for idx, c_text in enumerate(q['choices']):
                    choice_id = f"choice_{uuid.uuid4().hex[:10]}"
                    letter = letters[idx]
                    is_corr = 1 if letter == q['correct_answer_value'] else 0
                    cursor.execute('''
                        INSERT INTO choices (id, question_id, choice_letter, content, is_correct)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (choice_id, q_id, letter, c_text, is_corr))

            qs_inserted += 1

        print(f"[Seed Complete] Inserted {vocab_inserted} vocab terms and {qs_inserted} questions.")

if __name__ == '__main__':
    from app.database import init_db
    init_db()
    seed_all()
