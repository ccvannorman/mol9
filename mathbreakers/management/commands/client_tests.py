# NTA - New teacher account
# STU1C - Student 1 creates account
# STU1PX - Student 1 plays until playtime expired
# STU2C - Studnet 2 creates account
# STU2PX - Student 2 plays until playtime expired
# TBL1 - Teacher bought 1 license
# STU1J - Student 1 joins class with 1 license
# STU2J - Student 2 joins class with 1 license - should FAIL - "not enough licenses"

def get_playtime_limit_seconds(user):
	return get_num_teacher_students(user) * 3600

