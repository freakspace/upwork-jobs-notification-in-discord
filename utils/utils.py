import re
import json

def extract_info(job_posting):
    # Initialize result dictionary
    result = {
        'skills': None,
        'hourly_rate': None,
        'budget': None
    }
    
    # Check if 'summary' or 'summary_detail' or 'content' field exists in job_posting
    content_field = job_posting
    
    # Use regular expression to find hourly rate
    hourly_rate_match = re.search(r'Hourly Range</b>: \$(\d+\.\d+)-\$(\d+\.\d+)', content_field)
    if hourly_rate_match:
        result['hourly_rate'] = {
            'min': float(hourly_rate_match.group(1)),
            'max': float(hourly_rate_match.group(2))
        }
    
    # Use regular expression to find budget
    budget_match = re.search(r'budget</b>: \$([,\d]+)\s*-?\s*\$?([,\d]*)', content_field, re.IGNORECASE)
    if budget_match:
        min_budget = float(budget_match.group(1).replace(',', ''))
        max_budget = float(budget_match.group(2).replace(',', '')) if budget_match.group(2) else min_budget
        result['budget'] = {
            'min': min_budget,
            'max': max_budget
        }
    
    # Use regular expression to find skills
    skills_match = re.search(r'Skills</b>:\s*(.+)<br', content_field)
    if skills_match:
        result['skills'] = [skill.strip() for skill in skills_match.group(1).split(',')]
    
    return result