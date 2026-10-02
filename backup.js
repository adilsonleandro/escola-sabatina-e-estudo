// ============================================================
// SCRIPT DE BACKUP — Compreendendo a Bíblia
// ============================================================
// Como usar: node backup.js
// ============================================================

const fs = require('fs');
const path = require('path');

// Configuração
const BACKUP_DIR = 'backup';
const TIMESTAMP = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
const BACKUP_FOLDER = path.join(BACKUP_DIR, TIMESTAMP);

// Arquivos e pastas para backup
const ITEMS_TO_BACKUP = [
  'index.html',
  'licoes.html',
  'estudos.html',
  'estudo-detalhe.html',
  'estudo-professor.html',
  'tema-biblia.html',
  'css',
  'js'
];

// Criar pasta de backup
if (!fs.existsSync(BACKUP_DIR)) {
  fs.mkdirSync(BACKUP_DIR);
}

fs.mkdirSync(BACKUP_FOLDER, { recursive: true });

console.log('========================================');
console.log('BACKUP DO SITE — Compreendendo a Bíblia');
console.log('========================================');
console.log(`Data: ${new Date().toLocaleString()}`);
console.log(`Pasta: ${BACKUP_FOLDER}`);
console.log('----------------------------------------');

let successCount = 0;
let failCount = 0;

ITEMS_TO_BACKUP.forEach(item => {
  const source = path.join(__dirname, item);
  const dest = path.join(BACKUP_FOLDER, item);

  try {
    if (fs.existsSync(source)) {
      copyRecursive(source, dest);
      console.log(`✓ ${item}`);
      successCount++;
    } else {
      console.log(`✗ ${item} (não encontrado)`);
      failCount++;
    }
  } catch (err) {
    console.log(`✗ ${item} (erro: ${err.message})`);
    failCount++;
  }
});

console.log('----------------------------------------');
console.log(`Backup concluído: ${successCount} itens, ${failCount} erros`);
console.log(`Local: ${path.resolve(BACKUP_FOLDER)}`);
console.log('========================================');

// Função para copiar recursivamente
function copyRecursive(src, dest) {
  const stat = fs.statSync(src);

  if (stat.isDirectory()) {
    if (!fs.existsSync(dest)) {
      fs.mkdirSync(dest, { recursive: true });
    }
    fs.readdirSync(src).forEach(child => {
      copyRecursive(path.join(src, child), path.join(dest, child));
    });
  } else {
    fs.copyFileSync(src, dest);
  }
}
