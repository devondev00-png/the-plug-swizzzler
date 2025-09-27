import os
import json
from typing import Dict, Any, Optional
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class ExportService:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for export"""
        self.styles.add(ParagraphStyle(
            name='ScriptTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        ))
        
        self.styles.add(ParagraphStyle(
            name='ScriptMeta',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            textColor='gray'
        ))
        
        self.styles.add(ParagraphStyle(
            name='AgentDialogue',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            leftIndent=20,
            textColor='blue'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomerDialogue',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            leftIndent=20,
            textColor='green'
        ))
    
    def export_to_pdf(self, script_data: Dict[str, Any], filename: str) -> bool:
        """Export script to PDF format"""
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            
            # Add title
            title = f"Call Script - {script_data.get('company_name', 'Unknown Company')}"
            story.append(Paragraph(title, self.styles['ScriptTitle']))
            
            # Add metadata
            metadata = self._format_metadata(script_data)
            story.append(Paragraph(metadata, self.styles['ScriptMeta']))
            story.append(Spacer(1, 20))
            
            # Add script content
            script_content = script_data.get('script', '')
            formatted_script = self._format_script_for_pdf(script_content)
            story.append(Paragraph(formatted_script, self.styles['Normal']))
            
            # Build PDF
            doc.build(story)
            return True
            
        except Exception as e:
            print(f"PDF export failed: {e}")
            return False
    
    def export_to_txt(self, script_data: Dict[str, Any], filename: str) -> bool:
        """Export script to plain text format"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Add header
                f.write(f"Call Script - {script_data.get('company_name', 'Unknown Company')}\n")
                f.write("=" * 50 + "\n\n")
                
                # Add metadata
                metadata = self._format_metadata_txt(script_data)
                f.write(metadata + "\n\n")
                
                # Add script content
                f.write("SCRIPT CONTENT:\n")
                f.write("-" * 20 + "\n\n")
                f.write(script_data.get('script', ''))
                
            return True
            
        except Exception as e:
            print(f"TXT export failed: {e}")
            return False
    
    def export_to_json(self, script_data: Dict[str, Any], filename: str) -> bool:
        """Export script to JSON format"""
        try:
            export_data = {
                "export_info": {
                    "exported_at": datetime.utcnow().isoformat(),
                    "version": "1.0"
                },
                "script_data": script_data
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"JSON export failed: {e}")
            return False
    
    def _format_metadata(self, script_data: Dict[str, Any]) -> str:
        """Format metadata for PDF"""
        metadata_items = []
        
        if script_data.get('script_type'):
            metadata_items.append(f"<b>Script Type:</b> {script_data['script_type']}")
        if script_data.get('audience'):
            metadata_items.append(f"<b>Audience:</b> {script_data['audience']}")
        if script_data.get('tone'):
            metadata_items.append(f"<b>Tone:</b> {script_data['tone']}")
        if script_data.get('brand_voice'):
            metadata_items.append(f"<b>Brand Voice:</b> {script_data['brand_voice']}")
        if script_data.get('created_at'):
            metadata_items.append(f"<b>Generated:</b> {script_data['created_at']}")
        
        return "<br/>".join(metadata_items)
    
    def _format_metadata_txt(self, script_data: Dict[str, Any]) -> str:
        """Format metadata for text"""
        metadata_items = []
        
        if script_data.get('script_type'):
            metadata_items.append(f"Script Type: {script_data['script_type']}")
        if script_data.get('audience'):
            metadata_items.append(f"Audience: {script_data['audience']}")
        if script_data.get('tone'):
            metadata_items.append(f"Tone: {script_data['tone']}")
        if script_data.get('brand_voice'):
            metadata_items.append(f"Brand Voice: {script_data['brand_voice']}")
        if script_data.get('created_at'):
            metadata_items.append(f"Generated: {script_data['created_at']}")
        
        return "\n".join(metadata_items)
    
    def _format_script_for_pdf(self, script_content: str) -> str:
        """Format script content for PDF with proper styling"""
        lines = script_content.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                formatted_lines.append("<br/>")
                continue
            
            if line.startswith('Agent:'):
                # Format agent dialogue
                dialogue = line.replace('Agent:', '').strip()
                formatted_lines.append(f'<b>Agent:</b> {dialogue}')
            elif line.startswith('Customer:'):
                # Format customer dialogue
                dialogue = line.replace('Customer:', '').strip()
                formatted_lines.append(f'<b>Customer:</b> {dialogue}')
            else:
                # Regular text
                formatted_lines.append(line)
        
        return '<br/>'.join(formatted_lines)
    
    def create_script_package(self, script_data: Dict[str, Any], output_dir: str) -> Dict[str, str]:
        """Create a complete script package with multiple formats"""
        os.makedirs(output_dir, exist_ok=True)
        
        base_filename = f"script_{script_data.get('id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        files_created = {}
        
        # Export to different formats
        pdf_file = os.path.join(output_dir, f"{base_filename}.pdf")
        if self.export_to_pdf(script_data, pdf_file):
            files_created['pdf'] = pdf_file
        
        txt_file = os.path.join(output_dir, f"{base_filename}.txt")
        if self.export_to_txt(script_data, txt_file):
            files_created['txt'] = txt_file
        
        json_file = os.path.join(output_dir, f"{base_filename}.json")
        if self.export_to_json(script_data, json_file):
            files_created['json'] = json_file
        
        return files_created
