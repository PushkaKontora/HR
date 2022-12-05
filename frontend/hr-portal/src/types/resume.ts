export type ResumeUser = {
  'id': number,
  'owner': {
    'surname': string,
    'name': string,
    'patronymic': string,
    'email': string,
    'photo': string
  },
  'desired_job': string,
  'desired_salary': number,
  'experience': string,
  'document': string,
  'published_at': Date | string | null,
  'competencies': string[]
}