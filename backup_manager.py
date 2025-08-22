"""
Backup and restore utilities for Local AI Companion
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
import logging

class BackupManager:
    def __init__(self, project_root):
        self.project_root = project_root
        self.backup_dir = os.path.join(project_root, "data", "backups")
        self.logger = logging.getLogger(__name__)
    
    def create_full_backup(self):
        """Create a full backup of all user data"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"full_backup_{timestamp}.zip"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Backup config
                config_dir = os.path.join(self.project_root, "config")
                for root, dirs, files in os.walk(config_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, self.project_root)
                        zip_file.write(file_path, arc_path)
                
                # Backup data
                data_dir = os.path.join(self.project_root, "data")
                for root, dirs, files in os.walk(data_dir):
                    # Skip backup directory to avoid recursion
                    if "backups" in root:
                        continue
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, self.project_root)
                        zip_file.write(file_path, arc_path)
            
            self.logger.info(f"Full backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Failed to create full backup: {e}")
            return None
    
    def restore_backup(self, backup_path):
        """Restore from a backup file"""
        try:
            with zipfile.ZipFile(backup_path, 'r') as zip_file:
                zip_file.extractall(self.project_root)
            
            self.logger.info(f"Backup restored from: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            return False
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        try:
            for file in os.listdir(self.backup_dir):
                if file.endswith('.zip') or file.endswith('.json'):
                    file_path = os.path.join(self.backup_dir, file)
                    stat = os.stat(file_path)
                    backups.append({
                        'name': file,
                        'path': file_path,
                        'size': stat.st_size,
                        'created': datetime.fromtimestamp(stat.st_ctime)
                    })
        except Exception as e:
            self.logger.error(f"Failed to list backups: {e}")
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
