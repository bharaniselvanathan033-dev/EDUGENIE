"""
EduGenie Seminar Presentation Generator
Generates a professional .pptx file with 12 slides.
Dark navy theme with blue, purple, and cyan accents.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ─── Color Palette ────────────────────────────────────────────────
DARK_NAVY     = RGBColor(0x09, 0x0E, 0x1D)   # #090E1D — main background
PANEL_BG      = RGBColor(0x0C, 0x11, 0x22)   # #0C1122 — sidebar/cards
PANEL_BG2     = RGBColor(0x0D, 0x14, 0x29)   # #0D1429 — input fields
CARD_BORDER   = RGBColor(0x1A, 0x24, 0x40)   # subtle border
VIOLET        = RGBColor(0x8B, 0x7C, 0xFF)   # #8B7CFF — purple accent
VIOLET_BRIGHT = RGBColor(0xA5, 0x82, 0xFF)   # #A582FF
CYAN          = RGBColor(0x23, 0xCB, 0xDC)   # #23CBDC — cyan accent
CYAN_BRIGHT   = RGBColor(0x22, 0xD3, 0xEE)   # #22D3EE
BLUE          = RGBColor(0x3B, 0x82, 0xF6)   # #3B82F6 — blue accent
PINK          = RGBColor(0xEC, 0x48, 0x99)   # #EC4899 — quiz accent
WHITE         = RGBColor(0xF1, 0xF5, 0xF9)   # #F1F5F9 — headings
TEXT_LIGHT    = RGBColor(0xCB, 0xD5, 0xE1)   # #CBD5E1 — body text
TEXT_MUTED    = RGBColor(0x64, 0x74, 0x8B)   # #64748B — muted text
TEXT_DIM      = RGBColor(0x47, 0x55, 0x69)   # slate-600
GREEN         = RGBColor(0x4A, 0xDE, 0x80)   # #4ADE80 — success
AMBER         = RGBColor(0xFB, 0xBF, 0x24)   # #FBBF24 — warning

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

# ─── Helper Functions ─────────────────────────────────────────────

def add_bg(slide, color=DARK_NAVY):
    """Fill the entire slide with a solid background color."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    bg.shadow.inherit = False
    return bg

def add_glow(slide, left, top, width, height, color, opacity=0.12):
    """Add a decorative blurred-circle glow effect using a radial-ish oval."""
    glow = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, width, height)
    glow.fill.solid()
    glow.fill.fore_color.rgb = color
    glow.line.fill.background()
    glow.shadow.inherit = False
    # Can't do real blur in PPT, but the color + size gives the effect
    return glow

def add_text(slide, left, top, width, height, text, font_size=18, color=TEXT_LIGHT,
             bold=False, font_name='Calibri', alignment=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    """Add a simple text box."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox

def add_rich_text(slide, left, top, width, height, lines, font_size=16, color=TEXT_LIGHT,
                  font_name='Calibri', alignment=PP_ALIGN.LEFT, line_spacing=1.5, anchor=MSO_ANCHOR.TOP):
    """Add a text box with multiple paragraphs. Each line: (text, bold, color, size_override)."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for i, line in enumerate(lines):
        text, is_bold, line_color, size_override = line
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = text
        p.font.size = Pt(size_override if size_override else font_size)
        p.font.color.rgb = line_color if line_color else color
        p.font.bold = is_bold
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(6)
    return txBox

def add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None, border_width=Pt(1)):
    """Add a rounded rectangle shape."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = border_width
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    # Adjust corner radius
    try:
        shape.adjustments[0] = 0.06
    except:
        pass
    return shape

def add_rect(slide, left, top, width, height, fill_color, border_color=None):
    """Add a plain rectangle."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def add_accent_bar(slide, left, top, width=Inches(0.06), height=Inches(0.45), color=VIOLET):
    """Add a small vertical accent bar next to headings."""
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar

def add_slide_number(slide, num, total=12):
    """Add slide number at bottom right."""
    add_text(slide, Inches(12.0), Inches(7.0), Inches(1.2), Inches(0.4),
             f"{num} / {total}", font_size=10, color=TEXT_DIM, alignment=PP_ALIGN.RIGHT)

def add_notes(slide, notes_text):
    """Add speaker notes to a slide."""
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text

def add_gradient_rect(slide, left, top, width, height, color1, color2):
    """Add a rectangle with a two-color gradient fill."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    shape.shadow.inherit = False
    try:
        shape.adjustments[0] = 0.08
    except:
        pass
    # Use gradient fill
    fill = shape.fill
    fill.gradient()
    # python-pptx gradient stops
    fill.gradient_stops[0].color.rgb = color1
    fill.gradient_stops[0].position = 0.0
    fill.gradient_stops[1].color.rgb = color2
    fill.gradient_stops[1].position = 1.0
    return shape


# ════════════════════════════════════════════════════════════════
# SLIDE 1: TITLE
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
add_bg(slide)

# Decorative glows
add_glow(slide, Inches(-1.5), Inches(0.5), Inches(4), Inches(4), VIOLET, 0.08)
add_glow(slide, Inches(10.5), Inches(3.5), Inches(4), Inches(4), CYAN, 0.06)

# Logo icon — graduation cap circle
logo = add_rounded_rect(slide, Inches(5.67), Inches(0.8), Inches(2), Inches(2),
                         PANEL_BG, border_color=RGBColor(0x30, 0x3C, 0x60))
# Gradient circle for logo
logo_grad = add_gradient_rect(slide, Inches(6.0), Inches(1.1), Inches(1.35), Inches(1.35),
                               VIOLET, CYAN)
add_text(slide, Inches(6.0), Inches(1.15), Inches(1.35), Inches(1.35),
         "🎓", font_size=40, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Badge
badge = add_rounded_rect(slide, Inches(4.67), Inches(3.2), Inches(4), Inches(0.45),
                          RGBColor(0x0A, 0x11, 0x23), border_color=RGBColor(0x1B, 0x3A, 0x4D))
add_text(slide, Inches(4.67), Inches(3.22), Inches(4), Inches(0.45),
         "AI-POWERED LEARNING ASSISTANT", font_size=11, color=CYAN_BRIGHT, bold=True,
         alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Title
add_text(slide, Inches(1), Inches(3.9), Inches(11.333), Inches(1.2),
         "EduGenie", font_size=54, color=WHITE, bold=True,
         alignment=PP_ALIGN.CENTER, font_name='Calibri')

# Subtitle with gradient text effect (two text boxes)
add_text(slide, Inches(1), Inches(4.95), Inches(11.333), Inches(0.6),
         "Google Gemini Powered Learning Assistant", font_size=20, color=VIOLET_BRIGHT,
         bold=False, alignment=PP_ALIGN.CENTER)

# Decorative line
line = add_rect(slide, Inches(5.17), Inches(5.65), Inches(3), Inches(0.03), VIOLET)

# Bottom info
add_text(slide, Inches(1), Inches(6.1), Inches(11.333), Inches(0.4),
         "College Seminar Presentation", font_size=14, color=TEXT_MUTED,
         alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(6.55), Inches(11.333), Inches(0.4),
         "Department of Computer Science", font_size=12, color=TEXT_DIM,
         alignment=PP_ALIGN.CENTER)

add_notes(slide, "Good morning everyone. My name is [Your Name] and today I'm presenting my project, EduGenie — a Google Gemini Powered Learning Assistant. EduGenie is an AI-powered web application designed to help students learn more effectively. It uses Google's Gemini AI to answer questions, explain concepts, generate quizzes, summarize notes, and create personalized learning paths. Over the next few slides, I'll walk you through the problem it solves, how it works, and what makes it unique.")

# ════════════════════════════════════════════════════════════════
# SLIDE 2: INTRODUCTION
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(-1), Inches(-1), Inches(3.5), Inches(3.5), VIOLET, 0.06)

# Section label
add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "01 — INTRODUCTION", font_size=11, color=CYAN, bold=True)

# Heading with accent bar
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "What is EduGenie?", font_size=32, color=WHITE, bold=True)

# Main description
add_rich_text(slide, Inches(1.05), Inches(1.9), Inches(11), Inches(2.2),
    [
        ("EduGenie is an AI-powered learning assistant built for students.", False, TEXT_LIGHT, 17),
        ("It uses Google Gemini AI to provide five key learning tools in one platform:", False, TEXT_LIGHT, 17),
        ("", False, TEXT_LIGHT, 8),
        ("•  AI Question & Answer — Get instant answers to any study question", False, TEXT_LIGHT, 15),
        ("•  Concept Explanation — Break down difficult topics with simple analogies", False, TEXT_LIGHT, 15),
        ("•  Quiz Generator — Auto-create quizzes to test your knowledge", False, TEXT_LIGHT, 15),
        ("•  Text Summarizer — Summarize long notes into key points", False, TEXT_LIGHT, 15),
        ("•  Learning Path — Get a personalized step-by-step study plan", False, TEXT_LIGHT, 15),
    ], line_spacing=1.4)

# Bottom highlight card
card = add_rounded_rect(slide, Inches(1.05), Inches(5.2), Inches(11.2), Inches(1.3),
                         PANEL_BG, border_color=RGBColor(0x1B, 0x2A, 0x4D))
add_text(slide, Inches(1.4), Inches(5.35), Inches(2), Inches(0.35),
         "KEY HIGHLIGHT", font_size=9, color=CYAN, bold=True)
add_rich_text(slide, Inches(1.4), Inches(5.7), Inches(10.5), Inches(0.7),
    [
        ("Works with or without the AI backend — includes a built-in offline knowledge engine", True, WHITE, 14),
        ("so students can always learn, even without an internet connection to the Gemini API.", False, TEXT_MUTED, 13),
    ], line_spacing=1.3)

add_slide_number(slide, 2)
add_notes(slide, "EduGenie is essentially a one-stop learning platform powered by AI. Instead of switching between different tools — one for asking questions, another for quizzes, another for summaries — students get everything in one place. The five core features are: AI Q&A, concept explanation, quiz generation, text summarization, and learning path creation. What makes it special is the offline fallback — even if the Python backend isn't running, the app still works using a built-in knowledge engine. This was a deliberate design choice to make the app always available to students.")

# ════════════════════════════════════════════════════════════════
# SLIDE 3: PROBLEM STATEMENT
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(9.5), Inches(4), Inches(4), Inches(4), CYAN, 0.05)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "02 — PROBLEM STATEMENT", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "The Problem We Solve", font_size=32, color=WHITE, bold=True)

# Three problem cards
problems = [
    ("📚", "Information Overload", "Students struggle to find clear, simple explanations. Search results are often too complex or scattered across multiple websites.", VIOLET),
    ("🧪", "Lack of Practice", "Students read concepts but don't test themselves. Creating quizzes manually is time-consuming for both students and teachers.", CYAN),
    ("🛤️", "No Clear Path", "Students don't know what to learn first or in what order. They need a structured, step-by-step learning plan.", BLUE),
]

for i, (icon, title, desc, accent) in enumerate(problems):
    y = Inches(2.0 + i * 1.6)
    card = add_rounded_rect(slide, Inches(1.05), y, Inches(11.2), Inches(1.4),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Accent left bar
    add_accent_bar(slide, Inches(1.15), y + Inches(0.2), height=Inches(1.0), color=accent)
    # Icon
    add_text(slide, Inches(1.45), y + Inches(0.15), Inches(0.7), Inches(0.7),
             icon, font_size=24, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Title + description
    add_text(slide, Inches(2.3), y + Inches(0.15), Inches(9.5), Inches(0.4),
             title, font_size=16, color=WHITE, bold=True)
    add_text(slide, Inches(2.3), y + Inches(0.6), Inches(9.5), Inches(0.7),
             desc, font_size=13, color=TEXT_MUTED)

add_slide_number(slide, 3)
add_notes(slide, "Let me explain the three main problems EduGenie addresses. First, information overload — when students search for a topic online, they get thousands of results with varying levels of complexity. It's hard to find a clear, simple explanation. Second, lack of practice — students often read and understand a concept, but without testing themselves, the knowledge doesn't stick. Creating quizzes takes time. Third, no clear learning path — students don't always know what order to learn things in. They need structure. EduGenie solves all three problems in one platform.")

# ════════════════════════════════════════════════════════════════
# SLIDE 4: OBJECTIVES
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(-1), Inches(4), Inches(3.5), Inches(3.5), VIOLET, 0.05)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "03 — OBJECTIVES", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "Project Objectives", font_size=32, color=WHITE, bold=True)

objectives = [
    ("Provide AI-powered answers", "to student questions using Google Gemini", VIOLET),
    ("Simplify complex concepts", "with structured explanations and analogies", CYAN),
    ("Auto-generate quizzes", "for self-assessment on any topic", BLUE),
    ("Summarize study material", "into key points and takeaways", VIOLET),
    ("Create learning paths", "with step-by-step guidance and resources", CYAN),
    ("Ensure accessibility", "with offline fallback and responsive design", BLUE),
]

# 2x3 grid
for i, (title, desc, accent) in enumerate(objectives):
    col = i % 2
    row = i // 2
    x = Inches(1.05 + col * 5.8)
    y = Inches(2.0 + row * 1.55)
    card = add_rounded_rect(slide, x, y, Inches(5.4), Inches(1.35),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Number circle
    circle = add_gradient_rect(slide, x + Inches(0.2), y + Inches(0.3), Inches(0.65), Inches(0.65),
                                accent, VIOLET if accent == CYAN else CYAN)
    add_text(slide, x + Inches(0.2), y + Inches(0.3), Inches(0.65), Inches(0.65),
             str(i + 1), font_size=18, color=DARK_NAVY, bold=True,
             alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Text
    add_text(slide, x + Inches(1.05), y + Inches(0.2), Inches(4.2), Inches(0.4),
             title, font_size=15, color=WHITE, bold=True)
    add_text(slide, x + Inches(1.05), y + Inches(0.65), Inches(4.2), Inches(0.5),
             desc, font_size=12, color=TEXT_MUTED)

add_slide_number(slide, 4)
add_notes(slide, "These are the six main objectives of the project. First, provide AI-powered answers using Google Gemini — students can ask any question and get a clear answer. Second, simplify complex concepts with structured explanations that include analogies. Third, auto-generate quizzes so students can test themselves on any topic. Fourth, summarize study material — paste long notes and get key points. Fifth, create learning paths with step-by-step guidance and free resources. Sixth, ensure accessibility — the app works on mobile and desktop, and has an offline fallback so it always works even without the backend.")

# ════════════════════════════════════════════════════════════════
# SLIDE 5: TECHNOLOGIES USED
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(10), Inches(-1), Inches(4), Inches(4), CYAN, 0.05)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "04 — TECHNOLOGIES USED", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "Technology Stack", font_size=32, color=WHITE, bold=True)

tech_items = [
    ("Frontend", "React 18", "TypeScript", "Tailwind CSS", VIOLET),
    ("Backend", "Python", "FastAPI", "Uvicorn", CYAN),
    ("AI Engine", "Google Gemini", "gemini-1.5-flash", "API Integration", BLUE),
    ("Database", "Supabase", "PostgreSQL", "Study History", VIOLET),
    ("Build Tool", "Vite 5", "ESLint", "TypeScript", CYAN),
    ("Design", "Glassmorphism", "Responsive UI", "Dark Theme", BLUE),
]

for i, (category, t1, t2, t3, accent) in enumerate(tech_items):
    col = i % 3
    row = i // 3
    x = Inches(1.05 + col * 3.95)
    y = Inches(2.0 + row * 2.4)
    card = add_rounded_rect(slide, x, y, Inches(3.6), Inches(2.1),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Accent top border
    add_rect(slide, x + Inches(0.15), y + Inches(0.15), Inches(0.8), Inches(0.04), accent)
    # Category
    add_text(slide, x + Inches(0.25), y + Inches(0.3), Inches(3.1), Inches(0.35),
             category, font_size=10, color=accent, bold=True)
    # Tech items
    add_rich_text(slide, x + Inches(0.25), y + Inches(0.75), Inches(3.1), Inches(1.2),
        [
            (t1, True, WHITE, 15),
            (t2, False, TEXT_LIGHT, 14),
            (t3, False, TEXT_MUTED, 13),
        ], line_spacing=1.5)

add_slide_number(slide, 5)
add_notes(slide, "Let me walk through the technology stack. The frontend is built with React 18, TypeScript, and Tailwind CSS — this gives us a modern, type-safe, responsive UI. The backend is Python with FastAPI framework, served by Uvicorn — FastAPI is fast, modern, and has built-in validation. The AI engine is Google Gemini, specifically the gemini-1.5-flash model, integrated via the official Python SDK. The database is Supabase, which is PostgreSQL in the cloud — it stores study history so students can revisit past sessions. The build tool is Vite 5 for fast development. And the design uses glassmorphism with a dark navy theme and responsive layout.")

# ════════════════════════════════════════════════════════════════
# SLIDE 6: SYSTEM ARCHITECTURE
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "05 — SYSTEM ARCHITECTURE", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "How EduGenie Works", font_size=32, color=WHITE, bold=True)

# Architecture diagram — three layers with arrows
# Layer 1: Frontend
card1 = add_rounded_rect(slide, Inches(0.8), Inches(2.2), Inches(3.5), Inches(3.5),
                          PANEL_BG, border_color=VIOLET)
add_text(slide, Inches(0.9), Inches(2.35), Inches(3.3), Inches(0.35),
         "FRONTEND", font_size=10, color=VIOLET, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(0.9), Inches(2.8), Inches(3.3), Inches(0.5),
         "React App", font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rich_text(slide, Inches(1.1), Inches(3.4), Inches(2.9), Inches(2.2),
    [
        ("• Dashboard UI", False, TEXT_LIGHT, 12),
        ("• Feature Views", False, TEXT_LIGHT, 12),
        ("• API Client", False, TEXT_LIGHT, 12),
        ("• Offline Engine", False, TEXT_LIGHT, 12),
        ("• Supabase Client", False, TEXT_LIGHT, 12),
        ("• Tailwind CSS", False, TEXT_MUTED, 12),
    ], line_spacing=1.6)

# Arrow 1 →
add_text(slide, Inches(4.3), Inches(3.6), Inches(0.8), Inches(0.6),
         "→", font_size=28, color=CYAN, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(4.3), Inches(4.2), Inches(0.8), Inches(0.4),
         "HTTP", font_size=9, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

# Layer 2: Backend
card2 = add_rounded_rect(slide, Inches(5.1), Inches(2.2), Inches(3.5), Inches(3.5),
                          PANEL_BG, border_color=CYAN)
add_text(slide, Inches(5.2), Inches(2.35), Inches(3.3), Inches(0.35),
         "BACKEND", font_size=10, color=CYAN, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(5.2), Inches(2.8), Inches(3.3), Inches(0.5),
         "FastAPI Server", font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

add_rich_text(slide, Inches(5.4), Inches(3.4), Inches(2.9), Inches(2.2),
    [
        ("• /api/qa", False, TEXT_LIGHT, 12),
        ("• /api/explain", False, TEXT_LIGHT, 12),
        ("• /api/quiz", False, TEXT_LIGHT, 12),
        ("• /api/summarize", False, TEXT_LIGHT, 12),
        ("• /api/learning-path", False, TEXT_LIGHT, 12),
        ("• /api/health", False, TEXT_MUTED, 12),
    ], line_spacing=1.6)

# Arrow 2 →
add_text(slide, Inches(8.6), Inches(3.6), Inches(0.8), Inches(0.6),
         "→", font_size=28, color=BLUE, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(8.6), Inches(4.2), Inches(0.8), Inches(0.4),
         "API", font_size=9, color=TEXT_DIM, alignment=PP_ALIGN.CENTER)

# Layer 3: AI + Database
card3 = add_rounded_rect(slide, Inches(9.4), Inches(2.2), Inches(3.5), Inches(1.6),
                          PANEL_BG, border_color=BLUE)
add_text(slide, Inches(9.5), Inches(2.35), Inches(3.3), Inches(0.35),
         "AI ENGINE", font_size=10, color=BLUE, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(9.5), Inches(2.8), Inches(3.3), Inches(0.5),
         "Google Gemini", font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(9.5), Inches(3.3), Inches(3.3), Inches(0.4),
         "gemini-1.5-flash", font_size=12, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

card4 = add_rounded_rect(slide, Inches(9.4), Inches(4.1), Inches(3.5), Inches(1.6),
                          PANEL_BG, border_color=VIOLET)
add_text(slide, Inches(9.5), Inches(4.25), Inches(3.3), Inches(0.35),
         "DATABASE", font_size=10, color=VIOLET, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(9.5), Inches(4.7), Inches(3.3), Inches(0.5),
         "Supabase", font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(9.5), Inches(5.2), Inches(3.3), Inches(0.4),
         "PostgreSQL — Study History", font_size=11, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

# Security note at bottom
note_card = add_rounded_rect(slide, Inches(1.05), Inches(6.1), Inches(11.2), Inches(0.8),
                              RGBColor(0x0A, 0x11, 0x23), border_color=RGBColor(0x1B, 0x3A, 0x4D))
add_text(slide, Inches(1.4), Inches(6.15), Inches(2), Inches(0.35),
         "🔒 SECURITY", font_size=9, color=GREEN, bold=True)
add_text(slide, Inches(1.4), Inches(6.45), Inches(10.5), Inches(0.4),
         "The Gemini API key lives only in the backend .env file — it is never exposed to the frontend or the user's browser.",
         font_size=12, color=TEXT_LIGHT)

add_slide_number(slide, 6)
add_notes(slide, "This diagram shows the three-layer architecture. On the left is the Frontend — a React application that runs in the browser. It contains the dashboard UI, feature views for each tool, an API client that communicates with the backend, and a built-in offline knowledge engine as a fallback. The frontend sends HTTP requests to the Backend in the middle — a Python FastAPI server running on port 8000. The backend has six API endpoints, one for each feature plus a health check. On the right are the AI Engine and Database. The backend calls Google Gemini's API to generate responses, and Supabase stores the study history. The key security point is that the Gemini API key is stored only in the backend's environment file — it's never sent to the browser.")

# ════════════════════════════════════════════════════════════════
# SLIDE 7: PROJECT WORKFLOW
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "06 — PROJECT WORKFLOW", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "How a Request Flows", font_size=32, color=WHITE, bold=True)

# Workflow steps — horizontal flow
steps = [
    ("1", "Student Input", "User enters a topic\nor question + selects\nlearning level", VIOLET),
    ("2", "Frontend Sends\nRequest", "React app sends POST\nrequest to FastAPI\nbackend via API client", CYAN),
    ("3", "Backend Builds\nPrompt", "FastAPI constructs a\nGemini prompt with level\ncontext and instructions", BLUE),
    ("4", "Gemini AI\nGenerates", "Google Gemini processes\nthe prompt and returns\nan AI-powered response", VIOLET),
    ("5", "Result Displayed", "Response is shown in the\nUI and saved to Supabase\nfor study history", CYAN),
]

for i, (num, title, desc, accent) in enumerate(steps):
    x = Inches(0.6 + i * 2.6)
    y = Inches(2.3)
    # Card
    card = add_rounded_rect(slide, x, y, Inches(2.3), Inches(3.3),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Number circle
    circle = add_gradient_rect(slide, x + Inches(0.8), y + Inches(0.2), Inches(0.7), Inches(0.7),
                                accent, CYAN if accent == VIOLET else VIOLET)
    add_text(slide, x + Inches(0.8), y + Inches(0.2), Inches(0.7), Inches(0.7),
             num, font_size=22, color=DARK_NAVY, bold=True,
             alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Title
    add_text(slide, x + Inches(0.15), y + Inches(1.05), Inches(2), Inches(0.7),
             title, font_size=12, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    # Description
    add_text(slide, x + Inches(0.15), y + Inches(1.8), Inches(2), Inches(1.3),
             desc, font_size=10, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

    # Arrow between cards
    if i < 4:
        add_text(slide, x + Inches(2.3), y + Inches(1.3), Inches(0.35), Inches(0.5),
                 "→", font_size=20, color=accent, bold=True, alignment=PP_ALIGN.CENTER)

# Offline fallback note
fb_card = add_rounded_rect(slide, Inches(1.05), Inches(6.0), Inches(11.2), Inches(0.85),
                            RGBColor(0x0A, 0x11, 0x23), border_color=RGBColor(0x4A, 0x3A, 0x1D))
add_text(slide, Inches(1.4), Inches(6.05), Inches(3), Inches(0.35),
         "⚠️ OFFLINE FALLBACK", font_size=9, color=AMBER, bold=True)
add_text(slide, Inches(1.4), Inches(6.35), Inches(10.5), Inches(0.4),
         "If the backend is not running, step 2-4 are replaced by the built-in offline knowledge engine — the app always works.",
         font_size=12, color=TEXT_LIGHT)

add_slide_number(slide, 7)
add_notes(slide, "This slide shows how a typical request flows through the system. Step 1: The student enters a topic or question and selects their learning level — beginner, intermediate, or advanced. Step 2: The React frontend sends a POST request to the FastAPI backend. Step 3: The backend builds a carefully crafted prompt for Gemini, including the learning level context so the AI adjusts its language accordingly. Step 4: Google Gemini processes the prompt and returns an AI-generated response — this could be an answer, an explanation, a quiz, a summary, or a learning path. Step 5: The result is displayed in the UI and saved to Supabase for the student's study history. The important thing to note is the offline fallback — if the backend isn't running, steps 2 through 4 are replaced by the built-in knowledge engine, so the app always works.")

# ════════════════════════════════════════════════════════════════
# SLIDE 8: MAIN FEATURES
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "07 — MAIN FEATURES", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "Five Learning Tools in One", font_size=32, color=WHITE, bold=True)

features = [
    ("💬", "AI Q&A", "Ask any question\nGet instant AI answers\nwith examples", VIOLET),
    ("📖", "Explain", "Structured breakdown\nwith key points,\nanalogies, deep dive", CYAN),
    ("🧠", "Quiz", "Auto-generated quizzes\nwith 4 options,\nanswer checking", BLUE),
    ("📝", "Summarize", "Paste long notes\nGet key points &\ntakeaways instantly", PINK),
    ("🛤️", "Learning Path", "Step-by-step study\nplan with free\nresources per step", VIOLET),
]

for i, (icon, title, desc, accent) in enumerate(features):
    x = Inches(0.6 + i * 2.55)
    y = Inches(2.2)
    card = add_rounded_rect(slide, x, y, Inches(2.35), Inches(3.8),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Icon area
    icon_bg = add_rounded_rect(slide, x + Inches(0.65), y + Inches(0.3), Inches(1.05), Inches(1.05),
                                RGBColor(0x0D, 0x14, 0x29), border_color=accent)
    add_text(slide, x + Inches(0.65), y + Inches(0.3), Inches(1.05), Inches(1.05),
             icon, font_size=32, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Title
    add_text(slide, x + Inches(0.1), y + Inches(1.55), Inches(2.15), Inches(0.4),
             title, font_size=16, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    # Accent underline
    add_rect(slide, x + Inches(0.85), y + Inches(1.95), Inches(0.65), Inches(0.03), accent)
    # Description
    add_text(slide, x + Inches(0.15), y + Inches(2.15), Inches(2.05), Inches(1.5),
             desc, font_size=11, color=TEXT_MUTED, alignment=PP_ALIGN.CENTER)

# Study history card at bottom
hist_card = add_rounded_rect(slide, Inches(1.05), Inches(6.25), Inches(11.2), Inches(0.7),
                              PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
add_text(slide, Inches(1.4), Inches(6.3), Inches(3), Inches(0.35),
         "📊 BONUS FEATURE", font_size=9, color=GREEN, bold=True)
add_text(slide, Inches(1.4), Inches(6.55), Inches(10.5), Inches(0.35),
         "Study History — all sessions are saved to Supabase, so students can revisit past results anytime.",
         font_size=12, color=TEXT_LIGHT)

add_slide_number(slide, 8)
add_notes(slide, "These are the five main features of EduGenie, each accessible from the sidebar navigation. First is AI Q&A — students type any question and get an instant AI-powered answer with real-world examples. Second is Explain — enter a concept and get a structured breakdown with an overview, key points, an analogy, and a deeper explanation. Third is Quiz Generator — automatically creates multiple-choice quizzes with four options each, and students can check their answers with explanations. Fourth is Summarize — paste long notes or textbook passages and get the main idea, key points, and takeaways. Fifth is Learning Path — enter a subject and get a step-by-step study plan with free resources for each step. As a bonus, all sessions are saved to Study History so students can revisit their past work.")

# ════════════════════════════════════════════════════════════════
# SLIDE 9: WEBSITE SCREENSHOTS (UI MOCKUPS)
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "08 — WEBSITE PREVIEW", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "EduGenie Interface", font_size=32, color=WHITE, bold=True)

# --- Mockup 1: Dashboard ---
mock1 = add_rounded_rect(slide, Inches(0.6), Inches(2.0), Inches(6), Inches(4.6),
                          PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
add_text(slide, Inches(0.8), Inches(2.1), Inches(5.6), Inches(0.35),
         "Dashboard View", font_size=11, color=CYAN, bold=True)

# Sidebar mock
sidebar = add_rect(slide, Inches(0.75), Inches(2.5), Inches(1.3), Inches(4.0), PANEL_BG2)
add_text(slide, Inches(0.8), Inches(2.55), Inches(1.2), Inches(0.3),
         "🎓 EduGenie", font_size=8, color=WHITE, bold=True)
nav_items = ["Dashboard", "Ask Q&A", "Explain", "Quiz", "Summary", "Path"]
for j, item in enumerate(nav_items):
    is_active = j == 0
    txt_color = VIOLET_BRIGHT if is_active else TEXT_DIM
    add_text(slide, Inches(0.82), Inches(2.95 + j * 0.4), Inches(1.1), Inches(0.3),
             item, font_size=7, color=txt_color, bold=is_active)

# Dashboard content area
add_text(slide, Inches(2.2), Inches(2.6), Inches(4.2), Inches(0.3),
         "AI-POWERED LEARNING", font_size=7, color=CYAN, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(2.2), Inches(2.9), Inches(4.2), Inches(0.5),
         "Welcome to EduGenie", font_size=14, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)

# Feature cards in mockup
feat_mock = ["💬 Ask a Question", "📖 Explain a Concept", "🧠 Generate a Quiz", "📝 Summarize Notes"]
for j, feat in enumerate(feat_mock):
    col = j % 2
    row = j // 2
    fc = add_rounded_rect(slide, Inches(2.25 + col * 2.15), Inches(3.5 + row * 1.2), Inches(2.0), Inches(1.05),
                           RGBColor(0x0D, 0x14, 0x29), border_color=RGBColor(0x1A, 0x24, 0x40))
    add_text(slide, Inches(2.3 + col * 2.15), Inches(3.55 + row * 1.2), Inches(1.9), Inches(0.35),
             feat, font_size=8, color=WHITE, bold=True)

# Status badge
status = add_rounded_rect(slide, Inches(3.3), Inches(5.9), Inches(1.6), Inches(0.3),
                           RGBColor(0x0A, 0x11, 0x23), border_color=RGBColor(0x4A, 0x3A, 0x1D))
add_text(slide, Inches(3.3), Inches(5.9), Inches(1.6), Inches(0.3),
         "● Gemini Connected", font_size=7, color=GREEN, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# --- Mockup 2: Quiz Generator ---
mock2 = add_rounded_rect(slide, Inches(6.8), Inches(2.0), Inches(6), Inches(4.6),
                          PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
add_text(slide, Inches(7.0), Inches(2.1), Inches(5.6), Inches(0.35),
         "Quiz Generator View", font_size=11, color=CYAN, bold=True)

# Sidebar mock 2
sidebar2 = add_rect(slide, Inches(6.95), Inches(2.5), Inches(1.3), Inches(4.0), PANEL_BG2)
add_text(slide, Inches(7.0), Inches(2.55), Inches(1.2), Inches(0.3),
         "🎓 EduGenie", font_size=8, color=WHITE, bold=True)
for j, item in enumerate(nav_items):
    is_active = j == 3  # Quiz is active
    txt_color = VIOLET_BRIGHT if is_active else TEXT_DIM
    add_text(slide, Inches(7.02), Inches(2.95 + j * 0.4), Inches(1.1), Inches(0.3),
             item, font_size=7, color=txt_color, bold=is_active)

# Quiz content area
add_text(slide, Inches(8.4), Inches(2.6), Inches(4.2), Inches(0.35),
         "Generate a Quiz", font_size=13, color=WHITE, bold=True)
add_text(slide, Inches(8.4), Inches(2.95), Inches(4.2), Inches(0.25),
         "Test your understanding with auto-generated questions.", font_size=8, color=TEXT_MUTED)

# Level selector mock
for j, lvl in enumerate(["Beginner", "Intermediate", "Advanced"]):
    is_sel = j == 0
    lvl_card = add_rounded_rect(slide, Inches(8.45 + j * 1.45), Inches(3.35), Inches(1.35), Inches(0.55),
                                 RGBColor(0x0D, 0x14, 0x29),
                                 border_color=CYAN if is_sel else RGBColor(0x1A, 0x24, 0x40))
    add_text(slide, Inches(8.45 + j * 1.45), Inches(3.35), Inches(1.35), Inches(0.55),
             lvl, font_size=8, color=WHITE if is_sel else TEXT_DIM, bold=is_sel,
             alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Input field mock
input_mock = add_rounded_rect(slide, Inches(8.45), Inches(4.05), Inches(4.1), Inches(0.7),
                               RGBColor(0x0D, 0x14, 0x29), border_color=RGBColor(0x30, 0x3C, 0x60))
add_text(slide, Inches(8.6), Inches(4.05), Inches(3.8), Inches(0.7),
         "e.g. Newton's Laws...", font_size=9, color=TEXT_DIM, anchor=MSO_ANCHOR.MIDDLE)

# Generate button mock
btn = add_gradient_rect(slide, Inches(10.5), Inches(4.85), Inches(2.0), Inches(0.45),
                         VIOLET, CYAN)
add_text(slide, Inches(10.5), Inches(4.85), Inches(2.0), Inches(0.45),
         "Generate →", font_size=9, color=DARK_NAVY, bold=True,
         alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Quiz result mock
quiz_card = add_rounded_rect(slide, Inches(8.45), Inches(5.45), Inches(4.1), Inches(0.95),
                               RGBColor(0x0A, 0x11, 0x23), border_color=RGBColor(0x1B, 0x3A, 0x4D))
add_text(slide, Inches(8.6), Inches(5.5), Inches(3), Inches(0.25),
         "EDUGENIE SAYS", font_size=6, color=CYAN, bold=True)
add_text(slide, Inches(8.6), Inches(5.7), Inches(3), Inches(0.3),
         "1. Which best describes...", font_size=9, color=WHITE, bold=True)
add_text(slide, Inches(8.6), Inches(6.0), Inches(3), Inches(0.3),
         "○ Option A  ○ Option B", font_size=8, color=TEXT_LIGHT)

add_slide_number(slide, 9)
add_notes(slide, "These are mockups of the actual EduGenie interface. On the left is the Dashboard — the home page students see when they open the app. It shows the EduGenie logo, a welcome message, a Gemini connection status badge, and feature cards for all five tools. Each card is clickable and navigates to that feature. On the right is the Quiz Generator view. At the top is the feature title and description. Below that is the level selector — Beginner, Intermediate, or Advanced. Then a text input where the student enters the quiz topic, and a gradient Generate button. When clicked, the quiz appears below with multiple-choice questions and answer options. The design uses a dark navy theme with glassmorphism cards, violet and cyan accents, and is fully responsive on mobile.")

# ════════════════════════════════════════════════════════════════
# SLIDE 10: ADVANTAGES
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(9), Inches(4.5), Inches(4), Inches(4), CYAN, 0.05)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "09 — ADVANTAGES", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "Why EduGenie Stands Out", font_size=32, color=WHITE, bold=True)

advantages = [
    ("⚡", "Instant AI Responses", "Google Gemini delivers answers in seconds — no waiting, no searching through pages of results.", VIOLET),
    ("🎯", "Adaptive Learning Levels", "Three levels — Beginner, Intermediate, Advanced — so the AI adjusts its language and depth to match the student.", CYAN),
    ("🔧", "Always Works", "Offline fallback engine means the app functions even without the backend running — students are never blocked.", BLUE),
    ("📱", "Fully Responsive", "Works seamlessly on desktop, tablet, and mobile. Sidebar collapses to a drawer on smaller screens.", VIOLET),
    ("💾", "Study History", "Every session is saved to Supabase. Students can revisit past explanations, quizzes, and summaries anytime.", CYAN),
    ("🔒", "Secure by Design", "The Gemini API key lives only in the backend — it's never exposed in the frontend code or the user's browser.", BLUE),
]

for i, (icon, title, desc, accent) in enumerate(advantages):
    col = i % 2
    row = i // 2
    x = Inches(1.05 + col * 5.8)
    y = Inches(2.0 + row * 1.55)
    card = add_rounded_rect(slide, x, y, Inches(5.4), Inches(1.35),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Icon
    add_text(slide, x + Inches(0.2), y + Inches(0.2), Inches(0.6), Inches(0.6),
             icon, font_size=22, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Accent dot
    dot = add_rect(slide, x + Inches(0.95), y + Inches(0.15), Inches(0.04), Inches(1.05), accent)
    # Text
    add_text(slide, x + Inches(1.15), y + Inches(0.15), Inches(4.1), Inches(0.35),
             title, font_size=15, color=WHITE, bold=True)
    add_text(slide, x + Inches(1.15), y + Inches(0.55), Inches(4.1), Inches(0.7),
             desc, font_size=11, color=TEXT_MUTED)

add_slide_number(slide, 10)
add_notes(slide, "Here are six key advantages of EduGenie. First, instant AI responses — Gemini generates answers in seconds, much faster than searching through multiple websites. Second, adaptive learning levels — the student picks Beginner, Intermediate, or Advanced, and the AI adjusts its language and depth accordingly. This is a personalization feature. Third, always works — the offline fallback means even if the Python backend isn't running, students can still use the app with the built-in knowledge engine. Fourth, fully responsive — the UI works on desktop, tablet, and mobile, with the sidebar collapsing to a drawer on smaller screens. Fifth, study history — every session is saved to Supabase so students can revisit their work. Sixth, secure by design — the API key is never exposed to the browser.")

# ════════════════════════════════════════════════════════════════
# SLIDE 11: FUTURE ENHANCEMENTS
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(-1), Inches(3), Inches(3.5), Inches(3.5), VIOLET, 0.05)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "10 — FUTURE ENHANCEMENTS", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "What's Next for EduGenie", font_size=32, color=WHITE, bold=True)

enhancements = [
    ("👤", "User Accounts", "Add authentication so each student has a personal account with their own private study history and bookmarks.", VIOLET),
    ("🗣️", "Voice Input & Output", "Let students ask questions by speaking and hear answers read aloud — great for accessibility and hands-free learning.", CYAN),
    ("📊", "Progress Analytics", "Track quiz scores over time, show strengths and weaknesses, and suggest areas to focus on next.", BLUE),
    ("🌍", "Multi-Language Support", "Support multiple languages so students can learn in their native language, not just English.", VIOLET),
    ("🤝", "Teacher Dashboard", "Let teachers create custom quizzes and learning paths for their classes, and track student progress.", CYAN),
    ("📄", "PDF Export", "Allow students to export explanations, summaries, and learning paths as PDF documents for offline study.", BLUE),
]

for i, (icon, title, desc, accent) in enumerate(enhancements):
    col = i % 2
    row = i // 2
    x = Inches(1.05 + col * 5.8)
    y = Inches(2.0 + row * 1.55)
    card = add_rounded_rect(slide, x, y, Inches(5.4), Inches(1.35),
                             PANEL_BG, border_color=RGBColor(0x1A, 0x24, 0x40))
    # Icon
    add_text(slide, x + Inches(0.2), y + Inches(0.2), Inches(0.6), Inches(0.6),
             icon, font_size=22, alignment=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Accent dot
    dot = add_rect(slide, x + Inches(0.95), y + Inches(0.15), Inches(0.04), Inches(1.05), accent)
    # Text
    add_text(slide, x + Inches(1.15), y + Inches(0.15), Inches(4.1), Inches(0.35),
             title, font_size=15, color=WHITE, bold=True)
    add_text(slide, x + Inches(1.15), y + Inches(0.55), Inches(4.1), Inches(0.7),
             desc, font_size=11, color=TEXT_MUTED)

add_slide_number(slide, 11)
add_notes(slide, "While EduGenie is fully functional today, there are several enhancements I'd like to add in the future. First, user accounts — right now study history is shared, but with authentication, each student would have their own private history and bookmarks. Second, voice input and output — letting students ask questions by speaking and hearing answers read aloud would make the app more accessible. Third, progress analytics — tracking quiz scores over time to show strengths and weaknesses, and suggest what to study next. Fourth, multi-language support — so students can learn in their native language. Fifth, a teacher dashboard — letting teachers create custom quizzes and learning paths for their classes. Sixth, PDF export — allowing students to download their explanations, summaries, and learning paths as PDF documents for offline study.")

# ════════════════════════════════════════════════════════════════
# SLIDE 12: CONCLUSION
# ════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide)
add_glow(slide, Inches(-1), Inches(-1), Inches(4), Inches(4), VIOLET, 0.07)
add_glow(slide, Inches(10.5), Inches(4), Inches(4), Inches(4), CYAN, 0.06)

add_text(slide, Inches(0.8), Inches(0.5), Inches(4), Inches(0.35),
         "11 — CONCLUSION", font_size=11, color=CYAN, bold=True)
add_accent_bar(slide, Inches(0.8), Inches(1.0), height=Inches(0.55), color=VIOLET)
add_text(slide, Inches(1.05), Inches(0.95), Inches(10), Inches(0.7),
         "Conclusion", font_size=32, color=WHITE, bold=True)

# Summary text
add_rich_text(slide, Inches(1.05), Inches(2.0), Inches(11), Inches(2.0),
    [
        ("EduGenie demonstrates how AI can transform education.", True, WHITE, 18),
        ("", False, TEXT_LIGHT, 8),
        ("By combining Google Gemini with a modern web stack, it delivers five powerful", False, TEXT_LIGHT, 16),
        ("learning tools — Q&A, explanations, quizzes, summaries, and learning paths — in one", False, TEXT_LIGHT, 16),
        ("clean, student-friendly platform.", False, TEXT_LIGHT, 16),
    ], line_spacing=1.5)

# Key takeaways
add_text(slide, Inches(1.05), Inches(3.9), Inches(5), Inches(0.35),
         "KEY TAKEAWAYS", font_size=10, color=CYAN, bold=True)

takeaways = [
    ("AI makes learning faster", "Instant answers, no more searching through pages of results", VIOLET),
    ("Personalization matters", "Three learning levels adapt the AI's language to each student", CYAN),
    ("Always available", "Offline fallback ensures the app works even without the backend", BLUE),
]

for i, (title, desc, accent) in enumerate(takeaways):
    y = Inches(4.35 + i * 0.85)
    # Accent dot
    dot = add_gradient_rect(slide, Inches(1.1), y + Inches(0.1), Inches(0.12), Inches(0.12), accent, CYAN)
    add_text(slide, Inches(1.4), y, Inches(5), Inches(0.35),
             title, font_size=14, color=WHITE, bold=True)
    add_text(slide, Inches(1.4), y + Inches(0.35), Inches(10.5), Inches(0.35),
             desc, font_size=12, color=TEXT_MUTED)

# Thank you
add_text(slide, Inches(1), Inches(6.4), Inches(11.333), Inches(0.6),
         "Thank You!", font_size=28, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, Inches(1), Inches(7.0), Inches(11.333), Inches(0.35),
         "Questions & Discussion", font_size=14, color=VIOLET_BRIGHT, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 12)
add_notes(slide, "To conclude, EduGenie shows how AI can transform the way students learn. By combining Google Gemini with a modern web stack — React, FastAPI, and Supabase — it delivers five powerful learning tools in one clean platform. The key takeaways are: AI makes learning faster by giving instant answers, personalization matters because different students need different levels of explanation, and the app is always available thanks to the offline fallback. EduGenie is a working, production-ready application that's ready for real use. Thank you for listening. I'm happy to answer any questions you might have about the project, the technology, or the features.")

# ─── Save ────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "EduGenie_Seminar_Presentation.pptx")
prs.save(output_path)
print(f"Saved: {output_path}")
