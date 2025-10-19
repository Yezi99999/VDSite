import { marked } from 'marked';
import DOMPurify from 'dompurify';

// 配置marked选项
marked.setOptions({
  breaks: true, // 将换行符转换为<br>
  gfm: true,    // 启用GitHub风格的Markdown
  sanitize: false, // 禁用内置的sanitize，使用DOMPurify
});

/**
 * 将Markdown文本安全地转换为HTML
 * @param {string} markdownText - Markdown文本
 * @returns {string} 安全的HTML
 */
export function safeMarkdownToHtml(markdownText) {
  if (!markdownText) return '';
  
  try {
    // 将Markdown转换为HTML
    const rawHtml = marked.parse(markdownText);
    
    // 使用DOMPurify进行安全净化，防止XSS攻击
    const cleanHtml = DOMPurify.sanitize(rawHtml, {
      ALLOWED_TAGS: [
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'br', 'strong', 'em', 'code', 'pre',
        'blockquote', 'ul', 'ol', 'li',
        'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
        'hr', 'div', 'span'
      ],
      ALLOWED_ATTR: [
        'href', 'src', 'alt', 'title', 'class', 'id',
        'target', 'rel', 'width', 'height'
      ],
    });
    
    return cleanHtml;
  } catch (error) {
    console.error('Markdown解析错误:', error);
    // 如果解析失败，返回原始文本的HTML转义版本
    return markdownText
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>');
  }
}

/**
 * 预览Markdown文本
 * @param {string} markdownText - Markdown文本
 * @returns {string} 预览HTML
 */
export function previewMarkdown(markdownText) {
  return safeMarkdownToHtml(markdownText);
}