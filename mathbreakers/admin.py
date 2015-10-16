from django.contrib import admin

from mathbreakers.models import *

admin.site.register(LevelGroup)
admin.site.register(Level)
admin.site.register(EducationTopic)
admin.site.register(UserLevelState)
admin.site.register(UserTopicState)
admin.site.register(GalleryImage)
admin.site.register(Bug)
admin.site.register(CCLessonCategory)
admin.site.register(CCLessonGrade)
admin.site.register(CCLesson)
admin.site.register(Classroom)
admin.site.register(UserClassroomAssignment)
admin.site.register(PurchaseData)
admin.site.register(GamePurchase)
admin.site.register(GamePurchaseEmail)
admin.site.register(ButtonLog)
admin.site.register(ClassroomTeacherRel)
admin.site.register(PurchaseRecord)
admin.site.register(KickstarterRedirect)
admin.site.register(GameMenuClick)
admin.site.register(MathExperiment)
admin.site.register(EmailSurvey)
admin.site.register(EmailSurveyResponse)
admin.site.register(RoboterraLogin)
admin.site.register(PasswordReset)
admin.site.register(ClassroomActivityBin)
admin.site.register(RobotSentEmail)
admin.site.register(ClassroomSession)
admin.site.register(InventoryItem)
admin.site.register(TryLater)
admin.site.register(TeacherWaitlist)
admin.site.register(CohortTracking)
admin.site.register(TeacherSignupFlow)
admin.site.register(FullDownloadCodeEmailEntry)
admin.site.register(EducentsCode)

class UserUsernameAdmin(admin.ModelAdmin):
	search_fields=['user__username']
admin.site.register(HeatmapPoint, UserUsernameAdmin)
admin.site.register(UserProfile, UserUsernameAdmin)

class PreorderAdmin(admin.ModelAdmin):
	ordering=['-user']
admin.site.register(PreorderRegistration, PreorderAdmin)

class SkillsAdmin(admin.ModelAdmin):
	search_fields=['user__username']
	ordering=['skill_id']
admin.site.register(UserAdaptiveSkill, SkillsAdmin)

class ClassroomLogAdmin(admin.ModelAdmin):
	search_fields=['classroom__name', 'classroom__classroomteacherrel__user__username']
	ordering=['-date']
admin.site.register(ClassroomLog, ClassroomLogAdmin)