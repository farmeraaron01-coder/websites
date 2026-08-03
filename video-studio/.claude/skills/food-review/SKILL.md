---
name: food-review
description: The Mr Taco Shop food-review show format — campy, fast, dive-forward Mexican food reviews for YouTube. Use when cutting a food review, taco/burrito/taqueria video, restaurant visit or eating-to-camera piece. Covers the beat structure, take selection, B-roll grammar for food and location, the graphics kit, and YouTube packaging.
---

# Mr Taco Shop — food review format

Site: **mrtacoshop.com**. Tone: **campy, fast, affectionate**. The joke is
never on the restaurant. A dented counter, a hand-painted sign and a
twenty-year-old griddle are the *credentials* — the show treats a dive as a
place that has survived on the food alone, and finds that funny and admirable
at the same time. Punch at the format, at yourself, at the absurdity of caring
this much about a burrito. Never at the cook.

## The one rule

**Nothing dull survives.** A food review loses people in the first thirty
seconds and again at every slack moment after. If a shot is not doing one of
these three things, it is cut:

1. Making them hungry.
2. Making them laugh.
3. Telling them something they did not know.

"It's nice footage" is not one of the three. Neither is "it took a while to
get." Kill it.

## Beat structure

The order is deliberate: taste before context, always. Nobody stays for the
parking lot when they have not yet seen the food.

| Beat | Length | What it does |
|---|---|---|
| **COLD OPEN** | 0–8 s | The single best reaction in the whole shoot. Mid-bite, mid-sentence, no setup. Start on the strongest audio take available, whenever it was actually shot. |
| **TITLE** | 1–2 s | Show card. One beat, then gone. |
| **THE PLACE** | 10–25 s | The exterior, the sign, the room. This is where "old school building, dirty exterior" earns its keep — shot as texture and character, not as a complaint. |
| **THE ORDER** | 10–20 s | What was ordered and what it costs. Price chip on screen. |
| **THE FOOD** | 20–45 s | Macro B-roll. Steam, cheese pull, salsa, the cross-section. The hungriest part of the film. |
| **THE VERDICT** | 15–30 s | The actual review. Specific, not adjectives. Land on a score stamp. |
| **OUTRO** | 5–10 s | Where it is, what to order, mrtacoshop.com. Out fast. |

Target **3–6 minutes**. Under three feels thin for a review; over six and
retention falls off a cliff unless the place is genuinely remarkable.

A cold open that is not the best moment in the film is a wasted film.

## Take selection

Alternate takes of the same lines are normal on this show — the same thought
gets said three or four different ways across the shoot, often much later than
where it belongs in the cut. **Read the whole packed transcript before
choosing anything.** Group the alternates, then pick on:

1. **Delivery** — energy, timing, does the joke land.
2. **Cleanliness** — fewest restarts and hesitations.
3. **Specificity** — "the chorizo is rendered almost crispy" beats "it's
   really good" every time, even from a messier take.
4. **Mouth state** — a great line delivered through a full mouth is a B-roll
   cutaway, not a discard. Cover it and keep the audio.

Write the rejected takes into `edit/project.md` with the reason. On the next
episode that list is how you learn what the show sounds like when it works.

## B-roll grammar

The narration keeps running under every cutaway, so B-roll is free screen time
— but only if it is *doing* something.

**Food.** Cut in tight. A burrito on a plate at a normal distance is a
photograph; the same burrito filling the frame with steam coming off it is
appetite. Prioritise: the cross-section, the cheese pull, steam, the pour, the
first bite, sauce hitting the plate. Three to five seconds each.

**Location.** The peeling paint, the hand-lettered menu board, the griddle,
the order window, the cash-only sign. These are the show's texture. Cut them
in short — two to three seconds — and cluster them in THE PLACE rather than
sprinkling them through.

**Natural sound is half the shot.** Use `"audio": "duck"` on anything with a
sizzle, a crunch, a griddle scrape or street noise. Silent food B-roll is a
slideshow. `duck_db: -10` is the default; go to `-14` under a genuinely loud
sizzle so the nat sound briefly owns the moment.

```json
{"file": "footage/b_roll/griddle.MOV", "src_start": 4.2,
 "start_in_output": 61.5, "duration": 3.4,
 "mode": "full", "audio": "duck", "duck_db": -12,
 "note": "griddle scrape under 'they've had this thing since 1987'"}
```

**Cut away on a strong word, not into a pause.** Cutting away during silence
reads as a mistake. Come back to the face before the next idea starts.

## Graphics kit

Theme `campy` throughout. Built with `helpers/graphics.py`.

| Card | When | Notes |
|---|---|---|
| `title` | after the cold open | Show name + episode subject |
| `chapter` | between major beats | Sparingly — two or three per film, max |
| `lower_third` | first appearance of a dish | Dish name + what is in it |
| `price` | during THE ORDER | The real price. It is the most-commented number in any food video. |
| `stamp` | the verdict, and any big reaction | The punchline. Once or twice per film. |

Spell dish names correctly — al pastor, birria, barbacoa, carnitas, suadero,
chilaquiles, machaca, nopales. Pass a term list to `transcribe.py` via
`--prompt-file` so they come out right in the burned captions too. A
misspelled dish name is the fastest way to lose credibility with the exact
audience this show is for.

## Pacing

- Cut the moment a line lands. The most common fault in a first assembly is
  holding every shot two seconds too long.
- No shot longer than ~6 s without a cut, a push-in or a graphic.
- Run `autocut.py` for the hesitations, then tighten by hand for rhythm. The
  tool removes what is meaningless; you remove what is merely *fine*.
- Read the runtime after the first assembly and cut 20% more. It is always
  possible and it is always better.

## YouTube packaging

Deliver alongside the MP4, in `edit/youtube.md`:

- **Title** — the dish and the place, plus one hook of tension.
  "$8 Breakfast Burrito From A 40-Year-Old Gas Station Taqueria".
  No clickbait the video does not pay off.
- **Thumbnail frame** — pull a still: food filling the frame, face reacting,
  high contrast. Note its timecode. Frames come from `base.mkv`; a frame off
  the final carries the burned captions into the poster.
- **Description** — one-line summary, address, what to order, mrtacoshop.com.
- **Chapters** — timestamps from the beat structure. YouTube requires the
  first to be `0:00`.
- **Tags** — dish, city, cuisine, "food review".

**Never put the Tapatio count in the title, thumbnail, description or a chapter
name.** The score is the payoff and the only reason a viewer stays to the end —
printing it is printing the reason to skip. Pose it instead: "How many
Tapatios?" on the poster, answered in the verdict beat.

**Check a price before it becomes the hook.** The number said on camera at the
register is the *order total*, and an order usually has a drink in it. A title
built on "the $15 burrito" is a factual claim about a menu price, and the
transcript will not support it. Either quote the whole order or drop the price.

## Anti-patterns

- Opening on the exterior. Open on the food or the reaction.
- Silent food B-roll.
- Adjective-only reviews. "Amazing" tells the viewer nothing; "the tortilla is
  griddled hard enough to blister" tells them everything.
- Mocking the restaurant. Campy is affectionate; sneering is a different show.
- A stamp on every line. Scarcity is what makes it funny.
- Keeping a slow section because the footage was hard to get.
