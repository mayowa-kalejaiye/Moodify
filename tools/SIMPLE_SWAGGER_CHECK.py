#!/usr/bin/env python3
"""
Simple test of endpoint documentation
"""
import os
import sys
import re

def check_swagger_in_views():
    """Read the views.py file and check for swagger patterns"""
    
    print("🔍 CHECKING SWAGGER DOCUMENTATION IN VIEWS.PY")
    print("=" * 70)
    
    views_file = "mood_tracker/tracker/views.py"
    
    if not os.path.exists(views_file):
        print(f"❌ Views file not found: {views_file}")
        return False
    
    with open(views_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all class definitions
    class_pattern = r'class\s+(\w+)\s*\([^)]*\):'
    classes = re.findall(class_pattern, content)
    
    print(f"Found {len(classes)} classes:")
    
    # Find all swagger_auto_schema decorators
    swagger_pattern = r'@swagger_auto_schema\s*\('
    swagger_matches = re.findall(swagger_pattern, content)
    
    print(f"Found {len(swagger_matches)} @swagger_auto_schema decorators")
    
    # Check specific patterns that might indicate "No parameter needed"
    missing_patterns = []
    
    # Look for methods without proper parameter documentation
    method_pattern = r'def\s+(get|post|put|patch|delete)\s*\([^)]*\):'
    methods = re.findall(method_pattern, content)
    
    print(f"Found {len(methods)} HTTP methods")
    
    # Check for specific issues
    issues = []
    
    # Check if CommentListCreateAPIView has swagger decorators
    if 'class CommentListCreateAPIView' in content:
        comment_section = content[content.find('class CommentListCreateAPIView'):content.find('class CommentDetailAPIView')]
        if '@swagger_auto_schema' in comment_section:
            print("✅ CommentListCreateAPIView has Swagger documentation")
        else:
            issues.append("CommentListCreateAPIView missing Swagger documentation")
    
    # Check if CommentDetailAPIView has swagger decorators
    if 'class CommentDetailAPIView' in content:
        comment_detail_start = content.find('class CommentDetailAPIView')
        next_class = content.find('class MotivationSuggestionAPIView', comment_detail_start + 1)
        if next_class == -1:
            next_class = len(content)
        comment_detail_section = content[comment_detail_start:next_class]
        
        swagger_count = comment_detail_section.count('@swagger_auto_schema')
        if swagger_count >= 4:  # Should have GET, PUT, PATCH, DELETE
            print("✅ CommentDetailAPIView has comprehensive Swagger documentation")
        else:
            issues.append(f"CommentDetailAPIView has {swagger_count} swagger decorators, expected 4+ (GET, PUT, PATCH, DELETE)")
    
    # Check AISuggestionFeedbackAPIView
    if 'class AISuggestionFeedbackAPIView' in content:
        ai_feedback_start = content.find('class AISuggestionFeedbackAPIView')
        next_class = content.find('class ', ai_feedback_start + 1)
        if next_class == -1:
            next_class = len(content)
        ai_feedback_section = content[ai_feedback_start:next_class]
        
        if '@swagger_auto_schema' in ai_feedback_section:
            print("✅ AISuggestionFeedbackAPIView has Swagger documentation")
        else:
            issues.append("AISuggestionFeedbackAPIView missing Swagger documentation")
    
    # Check MoodPatternAnalysisAPIView
    if 'class MoodPatternAnalysisAPIView' in content:
        pattern_analysis_start = content.find('class MoodPatternAnalysisAPIView')
        next_class = content.find('class ', pattern_analysis_start + 1)
        if next_class == -1:
            next_class = len(content)
        pattern_analysis_section = content[pattern_analysis_start:next_class]
        
        if '@swagger_auto_schema' in pattern_analysis_section:
            print("✅ MoodPatternAnalysisAPIView has Swagger documentation")
        else:
            issues.append("MoodPatternAnalysisAPIView missing Swagger documentation")
    
    # Check for proper tags usage
    tags_pattern = r'tags=\[SWAGGER_TAGS\[[\'"]([^\'"]+)[\'"]]\]'
    tags_matches = re.findall(tags_pattern, content)
    
    print(f"Found {len(tags_matches)} properly tagged endpoints")
    print(f"Tags used: {set(tags_matches)}")
    
    print("\n" + "=" * 70)
    if issues:
        print(f"⚠️  ISSUES FOUND: {len(issues)}")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ ALL MAJOR ENDPOINTS HAVE PROPER SWAGGER DOCUMENTATION!")
        return True

if __name__ == "__main__":
    success = check_swagger_in_views()
    print(f"\n{'🎉 SWAGGER DOCUMENTATION CHECK COMPLETE!' if success else '⚠️ SOME ISSUES FOUND'}")
    sys.exit(0 if success else 1)
