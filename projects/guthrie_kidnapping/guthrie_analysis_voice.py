"""

The Nancy Guthrie Case: An Evidence-Based Analysis
Full narrated video - single scene

Render: manim guthrie_analysis_voice.py GuthrieAnalysisVoice

"""

from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Bypass manim-voiceover-plus v0.6.9 regression
# ---------------------------------------------------------------------------
import manim_voiceover_plus.services.base as _base

_original_set_transcription = _base.SpeechService.set_transcription


def _patched_set_transcription(self, model=None, kwargs=None):
    if model is None:
        self.transcription_model = None
        self._whisper_model = None
        return
    _original_set_transcription(self, model=model, kwargs=kwargs)


_base.SpeechService.set_transcription = _patched_set_transcription

# ---------------------------------------------------------------------------
from manim_voiceover_plus import VoiceoverScene
from manim_voiceover_plus.services.elevenlabs import ElevenLabsService
from elevenlabs import VoiceSettings

# ============================================================================
# OPTIMIZED CONFIGURATION - DO NOT MODIFY THESE VALUES
# ============================================================================
config.frame_height = 10
config.frame_width = 10 * 16 / 9
config.pixel_height = 1440
config.pixel_width = 2560
# ============================================================================

# ---------------------------------------------------------------------------
# Voice configuration
# ---------------------------------------------------------------------------
VOICE_ID = "rBgRd5IfS6iqrGfuhlKR"
MODEL_ID = "eleven_multilingual_v2"
VOICE_SETTINGS = VoiceSettings(
    stability=0.5,
    similarity_boost=0.75,
)

# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
BG_COLOR = "#0d1117"
ACCENT_RED = "#f85149"
ACCENT_GREEN = "#3fb950"
ACCENT_AMBER = "#d29922"
ACCENT_BLUE = "#58a6ff"
ACCENT_PURPLE = "#bc8cff"
CARD_BG = "#161b22"
BORDER_COLOR = "#30363d"
TEXT_PRIMARY = "#e6edf3"
TEXT_SECONDARY = "#8b949e"

# ---------------------------------------------------------------------------
# Narration script - all segments, all acts
# ---------------------------------------------------------------------------
SCRIPT = {
    # ACT 1: Cold open
    "cold_hook": (
        "On January thirty-first, twenty twenty-six, an eighty-four-year-old woman "
        "disappeared from her home in the Catalina Foothills of Tucson, Arizona. "
        "Within days, ransom notes demanding millions in Bitcoin appeared at three "
        "separate media outlets. But the deeper investigators looked, the less the "
        "ransom story held together."
    ),
    "cold_title": (
        "This is an analytical breakdown of the Nancy Guthrie disappearance. "
        "Not a recap of headlines. A structured look at what the available evidence "
        "actually tells us, and where the signal contradicts the noise."
    ),

    # ACT 2: Timeline
    "tl_intro": (
        "Before analyzing anything, we need to lay out what happened and when. "
        "The timeline matters because it reveals tempo, and tempo reveals intent."
    ),
    "tl_night": (
        "Sometime around one forty-seven a.m. on January thirty-first, a doorbell camera "
        "at the Guthrie residence captures a masked figure approaching the home. "
        "The figure wears a ski mask, gloves, and carries a backpack. What appears to be "
        "a holstered firearm is visible. The camera is defeated in stages: first by hand, "
        "then with foliage, then by physical damage."
    ),
    "tl_reported": (
        "Nancy is reported missing the following day, February first. "
        "Pima County Sheriff's Office responds. Homicide detectives are assigned, "
        "which signals that investigators are treating this as a serious crime from the start, "
        "not a welfare check."
    ),
    "tl_ransom": (
        "By February third, TMZ reports receiving an alleged ransom note demanding "
        "a substantial Bitcoin payment. The note includes a deadline and a threat. "
        "Matching notes also arrive at two Tucson television stations, KOLD and KGUN."
    ),
    "tl_deadlines": (
        "The first deadline is Thursday, February fifth. Four million dollars in Bitcoin. "
        "It passes with no payment and no consequences. "
        "The final deadline is Monday, February ninth. Six million dollars. "
        "That deadline also passes. The Bitcoin wallet shows zero transactions. "
        "The FBI states it is not aware of any continued communication "
        "between the family and suspected kidnappers."
    ),
    "tl_present": (
        "As of today, no suspect or person of interest has been publicly identified. "
        "No proof of life has been provided at any point. Nancy Guthrie has been missing "
        "for ten days."
    ),

    # ACT 3: Physical operation
    "phys_intro": (
        "Now let us isolate the physical operation at the house and evaluate it "
        "on its own terms. Forget the ransom for a moment. "
        "What does the intruder's behavior at the scene tell us?"
    ),
    "phys_preparation": (
        "The intruder arrives with a prepared kit. Ski mask, gloves, backpack, "
        "and what appears to be a holstered sidearm. This is not improvised. "
        "Someone selected these items in advance, which means there was a planning phase "
        "before the operation began."
    ),
    "phys_camera": (
        "The doorbell camera is neutralized in three deliberate stages. "
        "First, the intruder covers it by hand. Then obstructs it with foliage. "
        "Then physically damages the device. This is sequential escalation. "
        "It suggests the person knew the camera was there, tried a soft approach first, "
        "and moved to destructive methods only when needed."
    ),
    "phys_countersurv": (
        "Throughout the footage, the intruder maintains a head-down posture. "
        "That is a counter-surveillance behavior. It minimizes the chance of facial "
        "recognition or identification from overhead angles. Combined with the mask, "
        "it shows awareness of how modern residential security systems work."
    ),
    "phys_timing": (
        "The operational window is approximately one forty-seven a.m. "
        "Pre-dawn, deep into the sleep cycle, minimal neighbor activity. "
        "This is a deliberate timing choice, not a coincidence. "
        "Taken together, the physical operation shows planning, discipline, "
        "and awareness of security environments."
    ),

    # ACT 4: Ransom architecture
    "ransom_intro": (
        "Now let us look at the other side. The ransom operation that followed "
        "the physical event. If the break-in looked professional, "
        "the ransom architecture looks like a different person built it."
    ),
    "ransom_no_channel": (
        "The most fundamental problem is that the alleged kidnappers provided "
        "no reply channel. The ransom notes went to media outlets. Not to the family. "
        "Not to a lawyer. Not through a secure drop. To TMZ, KOLD, and KGUN. "
        "There is no documented way for the family to respond, negotiate, "
        "or even confirm receipt."
    ),
    "ransom_no_pol": (
        "In ten days, no verifiable proof of life has been provided. "
        "No photograph. No audio. No video. No item that only Nancy would have. "
        "The notes reference scene details like damaged property and clothing, "
        "but that information could come from someone who was at the house "
        "without necessarily having custody of the victim."
    ),
    "ransom_bitcoin": (
        "The Bitcoin wallet address included in the ransom note is real. "
        "It exists on-chain. But it has never been funded. Zero balance. "
        "Zero transactions. If this is a genuine kidnapping for ransom, "
        "the collection mechanism has never been activated."
    ),
    "ransom_deadlines": (
        "Two deadlines were set. Four million by Thursday. Six million by Monday. "
        "Both passed. No consequences were enforced. "
        "No proof was offered. The escalation was rhetorical, not operational."
    ),
    "ransom_media": (
        "Legitimate ransom operations are private. They use direct channels. "
        "They avoid media attention because publicity increases law enforcement pressure "
        "and decreases the chance of collecting payment. "
        "Broadcasting demands through news outlets is the opposite of how "
        "a functioning ransom operation works."
    ),

    # ACT 5: Competence gap (matches existing scene_05)
    "gap_title": (
        "This brings us to the central analytical tension in the case: "
        "the competence gap between the physical tradecraft and the ransom design."
    ),
    "gap_columns": (
        "On the left is the physical operation at the house. "
        "On the right is the ransom architecture that followed. "
        "They do not look like the work of the same level of operator."
    ),
    "gap_evidence": (
        "Physically, the intruder arrives masked, gloved, carrying a backpack and what appears "
        "to be a holstered firearm. They deliberately defeat the doorbell camera in stages and "
        "choose a narrow pre-dawn window. "
        "In contrast, the ransom side has no reply channel, no proof of life, "
        "an unfunded wallet, and deadlines that pass without consequence."
    ),
    "gap_gauges": (
        "If you rate the physical tradecraft, it looks like a high sophistication operation. "
        "If you rate the ransom design on its ability to actually collect money, it is very low."
    ),
    "gap_question": (
        "That gap raises the core analytical question: are we looking at one actor "
        "whose skills are uneven, or two different people splitting the work "
        "between on-scene action and off-scene communication?"
    ),

    # ACT 6: Bitcoin deep dive
    "btc_intro": (
        "The Bitcoin wallet deserves its own focus because it is the single "
        "most measurable piece of evidence in the ransom side of this case. "
        "Blockchain transactions are public. They do not lie."
    ),
    "btc_state": (
        "The wallet address provided in the ransom note has a confirmed zero balance. "
        "Zero inbound transactions. Zero outbound transactions. "
        "It was created but never used."
    ),
    "btc_comparison": (
        "In real ransomware and ransom-for-kidnapping operations, the payment "
        "infrastructure is typically prepared in advance. The wallet may receive "
        "a small test transaction. There may be multiple wallets. "
        "Tumbling or mixing services are sometimes pre-arranged to launder the payment "
        "once it arrives. None of that infrastructure exists here."
    ),
    "btc_interpretations": (
        "There are two ways to read this. "
        "One: the person who wrote the note does not understand how cryptocurrency "
        "collection actually works. "
        "Two: the ransom was never intended to be collected. "
        "The demand itself was the point, not the money."
    ),

    # ACT 7: Hypotheses
    "hyp_intro": (
        "With the evidence laid out, we can now frame the analytical hypotheses. "
        "These are not conclusions. They are structured possibilities that the "
        "available evidence either supports or weakens."
    ),
    "hyp_one": (
        "Hypothesis one: a single actor with uneven skills. "
        "One person planned and executed both the physical operation and the ransom. "
        "They were competent at breaking in but had no experience with "
        "kidnap-for-ransom logistics. This would explain the gap, "
        "but it requires accepting that someone disciplined enough to defeat cameras "
        "could not figure out how to set up a functional payment channel."
    ),
    "hyp_two": (
        "Hypothesis two: two or more actors with divided roles. "
        "The physical operator handled the scene. A separate person, less capable, "
        "handled the communication and ransom demands. "
        "This explains the competence gap naturally. "
        "But it raises new questions about coordination and motive sharing."
    ),
    "hyp_three": (
        "Hypothesis three: the ransom is a deliberate misdirection. "
        "The physical operation had a different objective entirely. "
        "The ransom notes were sent afterward to create a false narrative "
        "and redirect investigators toward a kidnapping framework "
        "that may not reflect what actually happened. "
        "This hypothesis treats the broken ransom architecture not as incompetence "
        "but as a feature. It was never meant to work."
    ),
    "hyp_weight": (
        "All three hypotheses are still on the table. "
        "But the zero-balance wallet, the absent proof of life, "
        "the one-way media broadcasts, and the unenforced deadlines "
        "all apply more pressure to hypothesis one than the other two. "
        "The simplest explanation has to carry a lot of contradictions."
    ),

    # ACT 8: Close
    "close_summary": (
        "Here is what we know with confidence. "
        "Someone with operational discipline entered Nancy Guthrie's home before dawn. "
        "Someone, possibly the same person, possibly not, sent ransom demands to the media "
        "with no functional way to collect. "
        "Two deadlines passed with no consequences. "
        "And after ten days, there is no proof of life and no suspect."
    ),
    "close_watch": (
        "Going forward, the things to watch are: "
        "whether any transaction ever hits that Bitcoin wallet, "
        "whether a communication channel is established privately that we do not know about, "
        "whether law enforcement shifts its framing away from kidnapping-for-ransom, "
        "and whether physical evidence from the scene produces a suspect. "
        "Each of those developments would shift the weight between the hypotheses."
    ),
    "close_final": (
        "This is not a story with a conclusion yet. "
        "But the evidence already on the table tells us something important: "
        "the ransom operation, as presented, does not function as a ransom operation. "
        "Whatever happened to Nancy Guthrie, the public framing may not match "
        "the underlying reality."
    ),
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def safe_position(mobject, max_y=4.0, min_y=-4.0):
    top = mobject.get_top()[1]
    bottom = mobject.get_bottom()[1]
    if top > max_y:
        mobject.shift(DOWN * (top - max_y))
    elif bottom < min_y:
        mobject.shift(UP * (min_y - bottom))
    return mobject


def section_transition(scene, old_group, new_title_text, new_subtitle_text=None):
    """Fade out old content, show a section title, return the title group."""
    if old_group is not None:
        scene.play(FadeOut(old_group), run_time=0.8)
        scene.wait(0.3)

    title = Text(new_title_text, font_size=40, weight=BOLD, color=TEXT_PRIMARY)
    parts = [title]
    if new_subtitle_text:
        sub = Text(new_subtitle_text, font_size=22, color=TEXT_SECONDARY)
        sub.next_to(title, DOWN, buff=0.35)
        parts.append(sub)
    group = VGroup(*parts).move_to(ORIGIN)
    return group


class GuthrieAnalysisVoice(VoiceoverScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        self.set_speech_service(
            ElevenLabsService(
                voice_id=VOICE_ID,
                model_id=MODEL_ID,
                voice_settings=VOICE_SETTINGS,
                transcription_model=None,
            )
        )

        # ===============================================================
        # ACT 1 - COLD OPEN
        # ===============================================================
        date_label = Text(
            "January 31, 2026", font_size=18, color=TEXT_SECONDARY,
        ).move_to(UP * 1.0)
        location_label = Text(
            "Catalina Foothills, Tucson, Arizona",
            font_size=16, color=TEXT_SECONDARY,
        ).next_to(date_label, DOWN, buff=0.25)

        with self.voiceover(text=SCRIPT["cold_hook"]):
            self.play(FadeIn(date_label, shift=UP * 0.2), run_time=0.8)
            self.play(FadeIn(location_label, shift=UP * 0.2), run_time=0.6)

        self.play(FadeOut(date_label), FadeOut(location_label), run_time=0.6)

        video_title = Text(
            "The Nancy Guthrie Case",
            font_size=46, weight=BOLD, color=TEXT_PRIMARY,
        )
        video_subtitle = Text(
            "An Evidence-Based Analysis",
            font_size=22, color=TEXT_SECONDARY,
        )
        video_subtitle.next_to(video_title, DOWN, buff=0.35)
        title_card = VGroup(video_title, video_subtitle).move_to(ORIGIN)

        with self.voiceover(text=SCRIPT["cold_title"]):
            self.play(FadeIn(video_title, shift=UP * 0.3), run_time=0.8)
            self.play(FadeIn(video_subtitle, shift=UP * 0.2), run_time=0.6)

        # ===============================================================
        # ACT 2 - TIMELINE
        # ===============================================================
        self.play(FadeOut(title_card), run_time=0.8)
        self.wait(0.3)

        act2_title = section_transition(
            self, None, "The Timeline", "Sequence of Known Events",
        )

        with self.voiceover(text=SCRIPT["tl_intro"]):
            self.play(FadeIn(act2_title, shift=UP * 0.3), run_time=0.8)

        # Shrink title to top
        act2_title.generate_target()
        act2_title.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act2_title), run_time=0.6)

        divider = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(divider), run_time=0.3)

        # Timeline bar
        tl_left = -6.5
        tl_right = 6.5
        tl_y = 2.5
        timeline_bar = Line(
            np.array([tl_left, tl_y, 0]),
            np.array([tl_right, tl_y, 0]),
            stroke_width=2, color=BORDER_COLOR,
        )
        self.play(Create(timeline_bar), run_time=0.5)

        # Timeline events
        events = [
            ("Jan 31", "1:47 AM\nIntrusion", tl_left + 0.5),
            ("Feb 1", "Reported\nMissing", tl_left + 2.8),
            ("Feb 3", "Ransom Notes\nto Media", tl_left + 5.1),
            ("Feb 5", "Deadline 1\n$4M", tl_left + 7.4),
            ("Feb 7", "Family\nVideo", tl_left + 9.7),
            ("Feb 9", "Deadline 2\n$6M", tl_left + 12.0),
        ]

        event_mobjects = VGroup()
        for date_str, desc_str, x_pos in events:
            dot = Dot(
                np.array([x_pos, tl_y, 0]),
                radius=0.08, color=ACCENT_BLUE,
            )
            date_txt = Text(date_str, font_size=12, weight=BOLD, color=TEXT_PRIMARY)
            date_txt.next_to(dot, UP, buff=0.15)
            desc_txt = Text(
                desc_str, font_size=10, color=TEXT_SECONDARY,
                line_spacing=0.8,
            )
            desc_txt.next_to(dot, DOWN, buff=0.15)
            node = VGroup(dot, date_txt, desc_txt)
            event_mobjects.add(node)

        # Night of intrusion
        with self.voiceover(text=SCRIPT["tl_night"]):
            self.play(FadeIn(event_mobjects[0], shift=UP * 0.2), run_time=0.6)

        # Reported missing
        with self.voiceover(text=SCRIPT["tl_reported"]):
            self.play(FadeIn(event_mobjects[1], shift=UP * 0.2), run_time=0.6)

        # Ransom notes
        with self.voiceover(text=SCRIPT["tl_ransom"]):
            self.play(FadeIn(event_mobjects[2], shift=UP * 0.2), run_time=0.6)

        # Deadlines
        with self.voiceover(text=SCRIPT["tl_deadlines"]):
            self.play(
                FadeIn(event_mobjects[3], shift=UP * 0.2),
                run_time=0.5,
            )
            self.play(
                FadeIn(event_mobjects[4], shift=UP * 0.2),
                run_time=0.5,
            )
            self.play(
                FadeIn(event_mobjects[5], shift=UP * 0.2),
                run_time=0.5,
            )

        # Present status
        day_counter = Text(
            "Day 10: No suspect. No proof of life.",
            font_size=20, weight=BOLD, color=ACCENT_AMBER,
        ).move_to(DOWN * 0.5)

        with self.voiceover(text=SCRIPT["tl_present"]):
            self.play(FadeIn(day_counter, shift=UP * 0.2), run_time=0.8)

        act2_all = VGroup(
            act2_title, divider, timeline_bar, event_mobjects, day_counter,
        )

        # ===============================================================
        # ACT 3 - PHYSICAL OPERATION
        # ===============================================================
        act3_title = section_transition(
            self, act2_all, "The Physical Operation", "Scene Analysis",
        )

        with self.voiceover(text=SCRIPT["phys_intro"]):
            self.play(FadeIn(act3_title, shift=UP * 0.3), run_time=0.8)

        act3_title.generate_target()
        act3_title.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act3_title), run_time=0.6)

        div3 = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(div3), run_time=0.3)

        # Preparation kit
        kit_items = ["Ski Mask", "Gloves", "Backpack", "Holstered Firearm"]
        kit_mobjects = VGroup()
        for i, item_text in enumerate(kit_items):
            box = RoundedRectangle(
                width=3.2, height=0.6, corner_radius=0.15,
                fill_color=CARD_BG, fill_opacity=1.0,
                stroke_color=ACCENT_GREEN, stroke_width=1.5,
            )
            label = Text(item_text, font_size=16, color=TEXT_PRIMARY)
            label.move_to(box)
            card = VGroup(box, label)
            kit_mobjects.add(card)
        kit_mobjects.arrange(RIGHT, buff=0.4).move_to(UP * 2.0)

        kit_label = Text(
            "Pre-staged equipment", font_size=14, color=TEXT_SECONDARY,
        ).next_to(kit_mobjects, DOWN, buff=0.25)

        with self.voiceover(text=SCRIPT["phys_preparation"]):
            for card in kit_mobjects:
                self.play(FadeIn(card, shift=UP * 0.2), run_time=0.4)
            self.play(FadeIn(kit_label), run_time=0.3)

        # Camera defeat sequence
        stages_data = [
            ("Stage 1", "Hand cover", ACCENT_GREEN),
            ("Stage 2", "Foliage obstruction", ACCENT_AMBER),
            ("Stage 3", "Physical damage", ACCENT_RED),
        ]
        stages_mobjects = VGroup()
        for i, (stage_title, stage_desc, color) in enumerate(stages_data):
            circle = Circle(
                radius=0.5, fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2,
            )
            s_title = Text(stage_title, font_size=14, weight=BOLD, color=color)
            s_desc = Text(stage_desc, font_size=11, color=TEXT_SECONDARY)
            s_title.next_to(circle, UP, buff=0.15)
            s_desc.next_to(circle, DOWN, buff=0.15)
            node = VGroup(circle, s_title, s_desc)
            stages_mobjects.add(node)
        stages_mobjects.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)

        # Arrows between stages
        arrows = VGroup()
        for i in range(2):
            a = Arrow(
                stages_mobjects[i].get_right(),
                stages_mobjects[i + 1].get_left(),
                buff=0.15, stroke_width=2, color=BORDER_COLOR,
            )
            arrows.add(a)

        escalation_label = Text(
            "Sequential Escalation", font_size=14, color=TEXT_SECONDARY,
        ).next_to(stages_mobjects, DOWN, buff=0.4)

        with self.voiceover(text=SCRIPT["phys_camera"]):
            for i in range(3):
                self.play(FadeIn(stages_mobjects[i], shift=UP * 0.2), run_time=0.5)
                if i < 2:
                    self.play(Create(arrows[i]), run_time=0.3)
            self.play(FadeIn(escalation_label), run_time=0.3)

        # Counter-surveillance
        cs_text = Text(
            "Head-down posture throughout footage",
            font_size=18, color=TEXT_PRIMARY,
        ).move_to(DOWN * 2.5)
        cs_detail = Text(
            "Counter-surveillance awareness of overhead camera angles",
            font_size=14, color=TEXT_SECONDARY,
        ).next_to(cs_text, DOWN, buff=0.15)

        with self.voiceover(text=SCRIPT["phys_countersurv"]):
            self.play(FadeIn(cs_text, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(cs_detail, shift=UP * 0.2), run_time=0.4)

        # Timing
        timing_label = Text(
            "Operational window: ~1:47 a.m.",
            font_size=18, weight=BOLD, color=ACCENT_GREEN,
        ).move_to(DOWN * 3.5)
        safe_position(timing_label)

        with self.voiceover(text=SCRIPT["phys_timing"]):
            self.play(FadeIn(timing_label, shift=UP * 0.2), run_time=0.6)

        act3_all = VGroup(
            act3_title, div3, kit_mobjects, kit_label,
            stages_mobjects, arrows, escalation_label,
            cs_text, cs_detail, timing_label,
        )

        # ===============================================================
        # ACT 4 - RANSOM ARCHITECTURE
        # ===============================================================
        act4_title = section_transition(
            self, act3_all, "The Ransom Architecture",
            "Communication and Collection Analysis",
        )

        with self.voiceover(text=SCRIPT["ransom_intro"]):
            self.play(FadeIn(act4_title, shift=UP * 0.3), run_time=0.8)

        act4_title.generate_target()
        act4_title.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act4_title), run_time=0.6)

        div4 = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(div4), run_time=0.3)

        # No reply channel
        sender_label = Text("Sender", font_size=16, color=TEXT_PRIMARY).move_to(
            LEFT * 5 + UP * 2.0
        )
        media_labels = VGroup()
        for i, name in enumerate(["TMZ", "KOLD", "KGUN"]):
            ml = Text(name, font_size=16, weight=BOLD, color=ACCENT_RED)
            ml.move_to(RIGHT * 2 + UP * (2.8 - i * 0.8))
            media_labels.add(ml)

        send_arrows = VGroup()
        for ml in media_labels:
            a = Arrow(
                sender_label.get_right(), ml.get_left(),
                buff=0.2, stroke_width=2, color=ACCENT_RED,
            )
            send_arrows.add(a)

        no_reply = Text(
            "No return path", font_size=16, weight=BOLD, color=ACCENT_RED,
        ).move_to(RIGHT * 2 + DOWN * 0.2)
        reply_x = Cross(
            stroke_color=ACCENT_RED, stroke_width=3,
        ).scale(0.25).next_to(no_reply, LEFT, buff=0.2)

        with self.voiceover(text=SCRIPT["ransom_no_channel"]):
            self.play(FadeIn(sender_label), run_time=0.3)
            for i in range(3):
                self.play(
                    Create(send_arrows[i]),
                    FadeIn(media_labels[i]),
                    run_time=0.4,
                )
            self.play(FadeIn(no_reply), FadeIn(reply_x), run_time=0.5)

        # Proof of life checklist
        channel_group = VGroup(
            sender_label, media_labels, send_arrows, no_reply, reply_x,
        )
        self.play(
            channel_group.animate.scale(0.6).move_to(LEFT * 4.5 + UP * 1.5),
            run_time=0.6,
        )

        pol_title = Text(
            "Proof of Life Checklist", font_size=16, weight=BOLD,
            color=TEXT_PRIMARY,
        ).move_to(RIGHT * 2.5 + UP * 2.5)
        pol_items_data = [
            "Photograph", "Audio recording", "Video",
            "Personal item", "Known-only phrase",
        ]
        pol_mobjects = VGroup()
        for i, item in enumerate(pol_items_data):
            x_mark = Text("X", font_size=14, weight=BOLD, color=ACCENT_RED)
            item_text = Text(item, font_size=14, color=TEXT_SECONDARY)
            row = VGroup(x_mark, item_text).arrange(RIGHT, buff=0.2)
            row.move_to(RIGHT * 2.5 + UP * (1.8 - i * 0.5))
            pol_mobjects.add(row)

        with self.voiceover(text=SCRIPT["ransom_no_pol"]):
            self.play(FadeIn(pol_title), run_time=0.3)
            for row in pol_mobjects:
                self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.35)

        # Bitcoin wallet
        btc_box = RoundedRectangle(
            width=6, height=1.2, corner_radius=0.2,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(DOWN * 1.5)
        btc_balance = Text(
            "Balance: 0.00000000 BTC", font_size=20, weight=BOLD,
            color=ACCENT_RED,
        ).move_to(btc_box.get_center() + UP * 0.15)
        btc_tx = Text(
            "Transactions: 0", font_size=14, color=TEXT_SECONDARY,
        ).move_to(btc_box.get_center() + DOWN * 0.25)

        with self.voiceover(text=SCRIPT["ransom_bitcoin"]):
            self.play(FadeIn(btc_box), run_time=0.3)
            self.play(FadeIn(btc_balance), FadeIn(btc_tx), run_time=0.5)

        # Deadlines
        dl_text = Text(
            "$4M deadline passed. $6M deadline passed. Zero consequences.",
            font_size=16, color=ACCENT_AMBER,
        ).move_to(DOWN * 3.0)
        safe_position(dl_text)

        with self.voiceover(text=SCRIPT["ransom_deadlines"]):
            self.play(FadeIn(dl_text, shift=UP * 0.2), run_time=0.6)

        # Media strategy
        media_note = Text(
            "Broadcasting demands to news outlets is the opposite\n"
            "of how functioning ransom operations work.",
            font_size=14, color=TEXT_SECONDARY, line_spacing=0.8,
        ).move_to(DOWN * 3.8)
        safe_position(media_note)

        with self.voiceover(text=SCRIPT["ransom_media"]):
            self.play(FadeIn(media_note, shift=UP * 0.2), run_time=0.6)

        act4_all = VGroup(
            act4_title, div4, channel_group,
            pol_title, pol_mobjects,
            btc_box, btc_balance, btc_tx,
            dl_text, media_note,
        )

        # ===============================================================
        # ACT 5 - COMPETENCE GAP
        # ===============================================================
        act5_title_group = section_transition(
            self, act4_all, "The Competence Gap",
            "Physical Tradecraft vs. Ransom Architecture",
        )

        with self.voiceover(text=SCRIPT["gap_title"]):
            self.play(FadeIn(act5_title_group, shift=UP * 0.3), run_time=0.8)

        act5_title_group.generate_target()
        act5_title_group.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act5_title_group), run_time=0.6)

        div5 = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(div5), run_time=0.3)

        col_left_x = -4.2
        col_right_x = 4.2
        col_top_y = 2.8

        phys_header = Text(
            "PHYSICAL TRADECRAFT", font_size=18, weight=BOLD, color=ACCENT_GREEN,
        ).move_to(np.array([col_left_x, col_top_y, 0]))
        ransom_header = Text(
            "RANSOM ARCHITECTURE", font_size=18, weight=BOLD, color=ACCENT_RED,
        ).move_to(np.array([col_right_x, col_top_y, 0]))

        with self.voiceover(text=SCRIPT["gap_columns"]):
            self.play(
                FadeIn(phys_header, shift=DOWN * 0.2),
                FadeIn(ransom_header, shift=DOWN * 0.2),
                run_time=0.6,
            )

        # Evidence rows
        phys_items = [
            ("Ski mask, gloves, backpack", "Prepared kit, not improvised"),
            ("Holstered firearm visible", "Coercive control capability"),
            ("Sequential camera defeat", "Hand, then foliage, then damage"),
            ("Head-down anti-ID posture", "Counter-surveillance awareness"),
            ("Pre-dawn timing", "Operational window at about 1:47 a.m."),
        ]
        ransom_items = [
            ("No reply channel provided", "Cannot negotiate or collect"),
            ("Zero proof of life", "Ten days, nothing verifiable"),
            ("Bitcoin wallet at zero", "Never funded, never used"),
            ("Deadlines pass, no action", "No consequences enforced"),
            ("One-way media broadcast", "Not how ransoms normally work"),
        ]

        def make_evidence_card(label_text, detail_text, color, x_center, y_pos):
            label = Text(label_text, font_size=16, color=TEXT_PRIMARY)
            detail = Text(detail_text, font_size=12, color=TEXT_SECONDARY)
            detail.next_to(label, DOWN, buff=0.1, aligned_edge=LEFT)
            text_group = VGroup(label, detail)
            indicator = Dot(radius=0.08, fill_opacity=1.0, color=color)
            row = VGroup(indicator, text_group).arrange(RIGHT, buff=0.25)
            row.move_to(np.array([x_center, y_pos, 0]))
            return row

        start_y = 1.9
        spacing = 0.85
        phys_mobjects = VGroup()
        ransom_mobjects = VGroup()

        for i, (label, detail) in enumerate(phys_items):
            y = start_y - i * spacing
            card = make_evidence_card(label, detail, ACCENT_GREEN, col_left_x, y)
            phys_mobjects.add(card)

        for i, (label, detail) in enumerate(ransom_items):
            y = start_y - i * spacing
            card = make_evidence_card(label, detail, ACCENT_RED, col_right_x, y)
            ransom_mobjects.add(card)

        with self.voiceover(text=SCRIPT["gap_evidence"]):
            for i in range(5):
                self.play(
                    FadeIn(phys_mobjects[i], shift=RIGHT * 0.3),
                    FadeIn(ransom_mobjects[i], shift=LEFT * 0.3),
                    run_time=0.6,
                )

        # Gauges
        gauge_y = -3.0
        gauge_w = 5.0

        phys_gauge_bg = RoundedRectangle(
            width=gauge_w, height=0.45, corner_radius=0.22,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(np.array([col_left_x, gauge_y, 0]))

        phys_gauge_fill = RoundedRectangle(
            width=0.01, height=0.35, corner_radius=0.17,
            fill_color=ACCENT_GREEN, fill_opacity=0.85, stroke_width=0,
        )
        phys_gauge_fill.move_to(phys_gauge_bg)
        phys_gauge_fill.align_to(phys_gauge_bg, LEFT).shift(RIGHT * 0.05)

        phys_gauge_label = Text(
            "HIGH", font_size=14, weight=BOLD, color=ACCENT_GREEN,
        ).next_to(phys_gauge_bg, RIGHT, buff=0.3)

        ransom_gauge_bg = RoundedRectangle(
            width=gauge_w, height=0.45, corner_radius=0.22,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(np.array([col_right_x, gauge_y, 0]))

        ransom_gauge_fill = RoundedRectangle(
            width=0.01, height=0.35, corner_radius=0.17,
            fill_color=ACCENT_RED, fill_opacity=0.85, stroke_width=0,
        )
        ransom_gauge_fill.move_to(ransom_gauge_bg)
        ransom_gauge_fill.align_to(ransom_gauge_bg, LEFT).shift(RIGHT * 0.05)

        ransom_gauge_label = Text(
            "LOW", font_size=14, weight=BOLD, color=ACCENT_RED,
        ).next_to(ransom_gauge_bg, RIGHT, buff=0.3)

        phys_gauge_title = Text(
            "Operational Sophistication", font_size=14, color=TEXT_SECONDARY,
        ).next_to(phys_gauge_bg, UP, buff=0.2)
        ransom_gauge_title = Text(
            "Collection Viability", font_size=14, color=TEXT_SECONDARY,
        ).next_to(ransom_gauge_bg, UP, buff=0.2)

        with self.voiceover(text=SCRIPT["gap_gauges"]):
            self.play(
                FadeIn(phys_gauge_bg), FadeIn(ransom_gauge_bg),
                FadeIn(phys_gauge_title), FadeIn(ransom_gauge_title),
                run_time=0.5,
            )
            phys_target = phys_gauge_fill.copy()
            phys_target.stretch_to_fit_width(gauge_w * 0.85)
            phys_target.move_to(phys_gauge_bg)
            phys_target.align_to(phys_gauge_bg, LEFT).shift(RIGHT * 0.05)

            ransom_target = ransom_gauge_fill.copy()
            ransom_target.stretch_to_fit_width(gauge_w * 0.15)
            ransom_target.move_to(ransom_gauge_bg)
            ransom_target.align_to(ransom_gauge_bg, LEFT).shift(RIGHT * 0.05)

            self.add(phys_gauge_fill, ransom_gauge_fill)
            self.play(
                Transform(phys_gauge_fill, phys_target),
                Transform(ransom_gauge_fill, ransom_target),
                run_time=2.0,
                rate_func=rate_functions.ease_out_cubic,
            )
            self.play(
                FadeIn(phys_gauge_label, shift=LEFT * 0.2),
                FadeIn(ransom_gauge_label, shift=LEFT * 0.2),
                run_time=0.4,
            )

        # Gap question
        gauge_group_bottom = VGroup(phys_gauge_bg, ransom_gauge_bg)
        gap_question = Text(
            "Same actor, or two different people?",
            font_size=24, weight=BOLD, color=ACCENT_AMBER,
        )
        gap_question.next_to(gauge_group_bottom, DOWN, buff=0.6)
        safe_position(gap_question, min_y=-4.6)

        with self.voiceover(text=SCRIPT["gap_question"]):
            self.play(FadeIn(gap_question, shift=UP * 0.3), run_time=0.8)

        act5_all = VGroup(
            act5_title_group, div5,
            phys_header, ransom_header,
            phys_mobjects, ransom_mobjects,
            phys_gauge_bg, phys_gauge_fill, phys_gauge_label, phys_gauge_title,
            ransom_gauge_bg, ransom_gauge_fill, ransom_gauge_label, ransom_gauge_title,
            gap_question,
        )

        # ===============================================================
        # ACT 6 - BITCOIN DEEP DIVE
        # ===============================================================
        act6_title = section_transition(
            self, act5_all, "The Bitcoin Problem", "On-Chain Evidence",
        )

        with self.voiceover(text=SCRIPT["btc_intro"]):
            self.play(FadeIn(act6_title, shift=UP * 0.3), run_time=0.8)

        act6_title.generate_target()
        act6_title.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act6_title), run_time=0.6)

        div6 = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(div6), run_time=0.3)

        # Wallet state
        wallet_box = RoundedRectangle(
            width=8, height=2.5, corner_radius=0.25,
            fill_color=CARD_BG, fill_opacity=1.0,
            stroke_color=BORDER_COLOR, stroke_width=1.5,
        ).move_to(UP * 1.0)

        wallet_title_txt = Text(
            "Ransom Wallet", font_size=18, weight=BOLD, color=TEXT_PRIMARY,
        ).move_to(wallet_box.get_top() + DOWN * 0.4)
        big_zero = Text(
            "0.00000000 BTC", font_size=36, weight=BOLD, color=ACCENT_RED,
        ).move_to(wallet_box.get_center())
        wallet_stats = Text(
            "Inbound: 0  |  Outbound: 0  |  Transactions: 0",
            font_size=14, color=TEXT_SECONDARY,
        ).move_to(wallet_box.get_bottom() + UP * 0.4)

        with self.voiceover(text=SCRIPT["btc_state"]):
            self.play(FadeIn(wallet_box), run_time=0.3)
            self.play(
                FadeIn(wallet_title_txt),
                FadeIn(big_zero),
                FadeIn(wallet_stats),
                run_time=0.6,
            )

        # Comparison to real ransoms
        real_flow_title = Text(
            "Standard Crypto Ransom Pipeline",
            font_size=16, weight=BOLD, color=TEXT_SECONDARY,
        ).move_to(DOWN * 1.2)

        flow_nodes = ["Victim\nWallet", "Payment\nWallet", "Mixer", "Exit\nWallets"]
        flow_mobjects = VGroup()
        for node_text in flow_nodes:
            box = RoundedRectangle(
                width=2.2, height=0.9, corner_radius=0.15,
                fill_color=CARD_BG, fill_opacity=1.0,
                stroke_color=BORDER_COLOR, stroke_width=1,
            )
            txt = Text(node_text, font_size=12, color=TEXT_SECONDARY, line_spacing=0.8)
            txt.move_to(box)
            flow_mobjects.add(VGroup(box, txt))
        flow_mobjects.arrange(RIGHT, buff=0.6).move_to(DOWN * 2.3)

        flow_arrows = VGroup()
        for i in range(3):
            a = Arrow(
                flow_mobjects[i].get_right(), flow_mobjects[i + 1].get_left(),
                buff=0.1, stroke_width=2, color=BORDER_COLOR,
            )
            flow_arrows.add(a)

        none_label = Text(
            "None of this exists in this case.",
            font_size=18, weight=BOLD, color=ACCENT_RED,
        ).move_to(DOWN * 3.4)
        safe_position(none_label)

        with self.voiceover(text=SCRIPT["btc_comparison"]):
            self.play(FadeIn(real_flow_title), run_time=0.3)
            self.play(
                *[FadeIn(n) for n in flow_mobjects],
                *[Create(a) for a in flow_arrows],
                run_time=0.8,
            )
            self.play(FadeIn(none_label, shift=UP * 0.2), run_time=0.5)

        # Two interpretations
        flow_group = VGroup(
            real_flow_title, flow_mobjects, flow_arrows, none_label,
        )
        self.play(
            flow_group.animate.scale(0.5).move_to(DOWN * 3.5 + LEFT * 4),
            run_time=0.5,
        )

        interp_a = VGroup(
            Text("Interpretation A", font_size=16, weight=BOLD, color=ACCENT_AMBER),
            Text("Incompetence", font_size=20, weight=BOLD, color=TEXT_PRIMARY),
            Text(
                "Does not understand crypto\ncollection mechanics",
                font_size=12, color=TEXT_SECONDARY, line_spacing=0.8,
            ),
        ).arrange(DOWN, buff=0.15).move_to(LEFT * 3 + DOWN * 1.5)

        interp_b = VGroup(
            Text("Interpretation B", font_size=16, weight=BOLD, color=ACCENT_AMBER),
            Text("Misdirection", font_size=20, weight=BOLD, color=TEXT_PRIMARY),
            Text(
                "Ransom was never intended\nto be collected",
                font_size=12, color=TEXT_SECONDARY, line_spacing=0.8,
            ),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 3 + DOWN * 1.5)

        or_text = Text("OR", font_size=18, weight=BOLD, color=ACCENT_AMBER).move_to(
            DOWN * 1.5
        )

        with self.voiceover(text=SCRIPT["btc_interpretations"]):
            self.play(FadeIn(interp_a, shift=RIGHT * 0.3), run_time=0.5)
            self.play(FadeIn(or_text), run_time=0.3)
            self.play(FadeIn(interp_b, shift=LEFT * 0.3), run_time=0.5)

        act6_all = VGroup(
            act6_title, div6,
            wallet_box, wallet_title_txt, big_zero, wallet_stats,
            flow_group, interp_a, interp_b, or_text,
        )

        # ===============================================================
        # ACT 7 - BEHAVIORAL HYPOTHESES
        # ===============================================================
        act7_title = section_transition(
            self, act6_all, "Behavioral Hypotheses",
            "Structured Analytical Possibilities",
        )

        with self.voiceover(text=SCRIPT["hyp_intro"]):
            self.play(FadeIn(act7_title, shift=UP * 0.3), run_time=0.8)

        act7_title.generate_target()
        act7_title.target.scale(0.55).move_to(UP * 4.0)
        self.play(MoveToTarget(act7_title), run_time=0.6)

        div7 = Line(
            LEFT * 7, RIGHT * 7, stroke_width=1, color=BORDER_COLOR,
            ).move_to(UP * 3.45)
        self.play(Create(div7), run_time=0.3)

        # Three hypothesis cards
        def make_hyp_card(number, title_text, strength, weakness, color, x_pos):
            card_bg = RoundedRectangle(
                width=4.8, height=4.5, corner_radius=0.2,
                fill_color=CARD_BG, fill_opacity=1.0,
                stroke_color=color, stroke_width=1.5,
            )
            num_label = Text(
                f"H{number}", font_size=14, weight=BOLD, color=color,
            )
            title_label = Text(
                title_text, font_size=18, weight=BOLD, color=TEXT_PRIMARY,
            )
            str_header = Text("Strength:", font_size=12, color=ACCENT_GREEN)
            str_text = Text(
                strength, font_size=12, color=TEXT_SECONDARY,
            )
            weak_header = Text("Weakness:", font_size=12, color=ACCENT_RED)
            weak_text = Text(
                weakness, font_size=12, color=TEXT_SECONDARY,
            )

            content = VGroup(
                num_label, title_label,
                VGroup(str_header, str_text).arrange(DOWN, buff=0.08, aligned_edge=LEFT),
                VGroup(weak_header, weak_text).arrange(DOWN, buff=0.08, aligned_edge=LEFT),
            ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            content.move_to(card_bg)

            card = VGroup(card_bg, content).move_to(np.array([x_pos, -0.3, 0]))
            return card

        h1 = make_hyp_card(
            1, "Single Actor",
            "Simplest explanation",
            "Skill gap is extreme",
            ACCENT_BLUE, -5.2,
        )
        h2 = make_hyp_card(
            2, "Split Operation",
            "Explains the gap naturally",
            "Raises coordination questions",
            ACCENT_PURPLE, 0,
        )
        h3 = make_hyp_card(
            3, "Misdirection",
            "Explains zero collection effort",
            "Requires deliberate deception",
            ACCENT_AMBER, 5.2,
        )

        with self.voiceover(text=SCRIPT["hyp_one"]):
            self.play(FadeIn(h1, shift=UP * 0.3), run_time=0.8)

        with self.voiceover(text=SCRIPT["hyp_two"]):
            self.play(FadeIn(h2, shift=UP * 0.3), run_time=0.8)

        with self.voiceover(text=SCRIPT["hyp_three"]):
            self.play(FadeIn(h3, shift=UP * 0.3), run_time=0.8)

        # Weight of evidence
        with self.voiceover(text=SCRIPT["hyp_weight"]):
            self.play(
                h1[0].animate.set_stroke(opacity=0.3),
                h1[1].animate.set_opacity(0.4),
                run_time=1.0,
            )

        act7_all = VGroup(act7_title, div7, h1, h2, h3)

        # ===============================================================
        # ACT 8 - CLOSE
        # ===============================================================
        self.play(FadeOut(act7_all), run_time=0.8)
        self.wait(0.3)

        facts = [
            "Someone with operational discipline entered the home before dawn.",
            "Someone sent ransom demands to the media with no way to collect.",
            "Two deadlines passed with no consequences.",
            "After ten days: no proof of life and no suspect.",
        ]
        fact_mobjects = VGroup()
        for i, fact_text in enumerate(facts):
            ft = Text(
                fact_text, font_size=18, color=TEXT_PRIMARY,
            ).move_to(UP * (1.5 - i * 1.0))
            fact_mobjects.add(ft)

        with self.voiceover(text=SCRIPT["close_summary"]):
            for ft in fact_mobjects:
                self.play(FadeIn(ft, shift=UP * 0.2), run_time=0.6)

        # What to watch
        self.play(
            fact_mobjects.animate.scale(0.6).move_to(UP * 3.0),
            run_time=0.6,
        )

        watch_title = Text(
            "What to Watch For", font_size=22, weight=BOLD, color=ACCENT_AMBER,
        ).move_to(UP * 1.2)

        watch_items = [
            "Any transaction hitting the Bitcoin wallet",
            "A private communication channel we do not know about",
            "Law enforcement reframing away from kidnapping-for-ransom",
            "Physical evidence producing a suspect",
        ]
        watch_mobjects = VGroup()
        for i, item in enumerate(watch_items):
            bullet = Text(
                f"  {item}", font_size=16, color=TEXT_PRIMARY,
            ).move_to(UP * (0.3 - i * 0.6))
            watch_mobjects.add(bullet)

        with self.voiceover(text=SCRIPT["close_watch"]):
            self.play(FadeIn(watch_title), run_time=0.4)
            for wb in watch_mobjects:
                self.play(FadeIn(wb, shift=RIGHT * 0.2), run_time=0.5)

        # Final statement
        close_group = VGroup(fact_mobjects, watch_title, watch_mobjects)
        self.play(FadeOut(close_group), run_time=0.8)

        final_line = Text(
            "The ransom operation, as presented,\n"
            "does not function as a ransom operation.",
            font_size=24, weight=BOLD, color=TEXT_PRIMARY,
            line_spacing=1.0,
        ).move_to(UP * 0.5)

        date_stamp = Text(
            "Analysis current as of February 10, 2026",
            font_size=14, color=TEXT_SECONDARY,
        ).move_to(DOWN * 1.5)

        with self.voiceover(text=SCRIPT["close_final"]):
            self.play(FadeIn(final_line, shift=UP * 0.3), run_time=1.0)
            self.play(FadeIn(date_stamp), run_time=0.5)

        self.wait(3.0)
        self.play(FadeOut(final_line), FadeOut(date_stamp), run_time=1.5)
        self.wait(0.5)
