const express = require('express');
const router = express.Router();
const fs = require('fs');
const path = require('path');

let canonData = { chapters: [] };
let diagramsData = { diagrams: [] };

function initializeCanon() {
  try {
    const canonJsonPath = path.join(__dirname, '../data/canon.json');
    if (fs.existsSync(canonJsonPath)) {
      canonData = JSON.parse(fs.readFileSync(canonJsonPath, 'utf8'));
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

function initializeDiagrams() {
  try {
    const diagramsJsonPath = path.join(__dirname, '../data/diagrams.json');
    if (fs.existsSync(diagramsJsonPath)) {
      diagramsData = JSON.parse(fs.readFileSync(diagramsJsonPath, 'utf8'));
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

initializeCanon();
initializeDiagrams();

router.get('/canon/toc', (req, res) => {
  const toc = canonData.chapters.map(ch => ({
    id: ch.id,
    section: ch.section,
    title: ch.title,
    description: ch.description,
    subsections: ch.subsections ? ch.subsections.map(s => s.title) : []
  }));
  res.json({ toc, total: toc.length });
});

router.get('/canon/chapters/:id', (req, res) => {
  const chapter = canonData.chapters.find(ch => ch.id === req.params.id);
  if (!chapter) {
    return res.status(404).json({ error: 'Chapter not found' });
  }
  const currentIndex = canonData.chapters.findIndex(ch => ch.id === req.params.id);
  const prevChapter = currentIndex > 0 ? canonData.chapters[currentIndex - 1] : null;
  const nextChapter = currentIndex < canonData.chapters.length - 1 ? canonData.chapters[currentIndex + 1] : null;
  res.json({
    ...chapter,
    prev: prevChapter ? { id: prevChapter.id, title: prevChapter.title } : null,
    next: nextChapter ? { id: nextChapter.id, title: nextChapter.title } : null
  });
});

router.get('/canon/search', (req, res) => {
  const query = (req.query.q || '').toLowerCase();
  if (!query || query.length < 2) {
    return res.json({ results: [] });
  }
  const results = [];
  canonData.chapters.forEach(chapter => {
    if (chapter.title.toLowerCase().includes(query) || chapter.description.toLowerCase().includes(query) || chapter.content.toLowerCase().includes(query)) {
      results.push({
        type: 'chapter',
        id: chapter.id,
        section: chapter.section,
        title: chapter.title,
        excerpt: chapter.description
      });
    }
  });
  res.json({ results: results.slice(0, 20) });
});

router.get('/diagrams', (req, res) => {
  const diagrams = diagramsData.diagrams.map(d => ({
    id: d.id,
    title: d.title,
    category: d.category,
    description: d.description,
    tags: d.tags || []
  }));
  res.json({ diagrams, total: diagrams.length });
});

router.get('/diagrams/:id', (req, res) => {
  const diagram = diagramsData.diagrams.find(d => d.id === req.params.id);
  if (!diagram) {
    return res.status(404).json({ error: 'Diagram not found' });
  }
  try {
    const svgPath = path.join(__dirname, '../public/diagrams', diagram.file);
    let svgContent = '';
    if (fs.existsSync(svgPath)) {
      svgContent = fs.readFileSync(svgPath, 'utf8');
    } else {
      svgContent = `<svg viewBox="0 0 680 500"><text x="340" y="250" text-anchor="middle" fill="#999">File not found: ${diagram.file}</text></svg>`;
    }
    res.json({
      id: diagram.id,
      title: diagram.title,
      category: diagram.category,
      description: diagram.description,
      tags: diagram.tags || [],
      related_chapters: diagram.related_chapters || [],
      svg: svgContent
    });
  } catch (error) {
    res.status(500).json({ error: 'Error loading diagram' });
  }
});

router.post('/diagrams/:id/view', (req, res) => {
  const diagram = diagramsData.diagrams.find(d => d.id === req.params.id);
  if (!diagram) return res.status(404).json({ error: 'Not found' });
  console.log(`Viewed: ${diagram.title}`);
  res.json({ success: true });
});

module.exports = router;
