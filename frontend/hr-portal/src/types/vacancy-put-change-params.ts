export interface VacancyPutChangeParams {
  name: string,
  description: string,
  expected_experience: string,
  salary_from: number | null,
  salary_to: number | null,
  published: boolean
}