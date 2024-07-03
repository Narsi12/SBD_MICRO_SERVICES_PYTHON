import uuid
from django.db import models

class LanguageLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=100, null=False, unique=True)
    language_abbreviation = models.CharField(max_length=2, null=False, unique=True)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'language_lkp'

    def __str__(self):
        return self.language

class FileTypeLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_type = models.CharField(max_length=100, null=False, unique=True)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'file_type_lkp'

    def __str__(self):
        return self.file_type

class StatusLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=100, null=False, unique=True)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'status_lkp'

    def __str__(self):
        return self.status

class AdGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    original_folder_url = models.CharField(max_length=255, null=False)
    translated_folder_url = models.CharField(max_length=255, null=False)
    review_folder_url = models.CharField(max_length=255, null=False)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'ad_group'

    def __str__(self):
        return self.name

class AdGroupUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ad_group_id = models.ForeignKey(AdGroup, on_delete=models.PROTECT, null=False, db_column='ad_group_id')
    user_id = models.UUIDField(null=False)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'ad_group_user'

    def __str__(self):
        return self.user_id

class TranslationBatch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translator_user_id = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'translation_batch'

    def __str__(self):
        return self.translator_user_id

class Glossary(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)
    language_lkp_id = models.ForeignKey(LanguageLkp, on_delete=models.PROTECT, null=False, db_column='language_lkp_id')
    department_lkp_id = models.UUIDField(null=False)
    file_blob_path = models.CharField(max_length=255, null=False)
    created_by = models.UUIDField(null=False)
    created_by_datetime = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_datetime = models.DateTimeField(null=True)

    class Meta:
        db_table = 'glossary'
    
    def __str__(self):
        return self.name

class Translation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translation_batch_id = models.ForeignKey(TranslationBatch, on_delete=models.PROTECT, null=False, db_column='translation_batch_id')
    file_type_lkp_id = models.ForeignKey(FileTypeLkp, on_delete=models.PROTECT, null=False, db_column='file_type_lkp_id')
    status_lkp_id = models.ForeignKey(StatusLkp, on_delete=models.PROTECT, null=False, db_column='status_lkp_id')
    glossary_id = models.ForeignKey(Glossary, on_delete=models.PROTECT, null=False, db_column='glossary_id')
    source_language_id = models.ForeignKey(LanguageLkp, on_delete=models.PROTECT, related_name='source_language', null=False, db_column='base_language_id')
    target_language_id = models.ForeignKey(LanguageLkp, on_delete=models.PROTECT, related_name='target_language', null=False, db_column='translate_language_id')
    reviewer_user_id = models.UUIDField(unique=True)
    ad_group_id = models.ForeignKey(AdGroup, on_delete=models.PROTECT, related_name='ad_group',null=False, db_column='ad_group_id')
    file_name = models.CharField(max_length=100, null=False, unique=True)
    due_date = models.DateTimeField(null=False)
    source_file_blob_path = models.CharField(max_length=255, null=False)
    translated_file_blob_path = models.CharField(max_length=255, null=False)
    reviewed_file_blob_path = models.CharField(max_length=255)
    translation_feedback = models.CharField(max_length=500)
    sharepoint_source_file_path = models.CharField(max_length=255)
    sharepoint_target_file_path = models.CharField(max_length=255)

    class Meta:
        db_table = 'translation'

    def __str__(self):
        return self.file_name

class TranslationActionLkp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=100, null=False, unique=True)
    created_by = models.UUIDField(null=False)
    created_by_date = models.DateTimeField(auto_now_add=True,null=False)
    updated_by = models.UUIDField(null=True)
    updated_by_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'translation_action_lkp'

    def __str__(self):
        return self.action

class Translation_log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    translation_id = models.ForeignKey(Translation, on_delete=models.PROTECT, null=False, db_column='translation_id')
    action_by_user_id = models.UUIDField(null=False)
    translation_action_lkp_id = models.ForeignKey(TranslationActionLkp, on_delete=models.PROTECT, null=False, db_column='translation_action_lkp_id')
    action_datetime = models.DateTimeField(auto_now_add=True,null=False)

    class Meta:
        db_table = 'translation_log'

    def __str__(self):
        return self.translation_id