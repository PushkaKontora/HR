import {ResumeFieldContainer, ResumeFieldLabel} from '../styled/resume/styles';
import {CompetencyFlexContainer} from '../styled/values/competency-flex-container';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {ResumeTitle} from '../styled/resume/resume-title';
import {ExperienceOptions} from '../../types/experience-options';
import {CompetencyList} from '../competency-list/competency-list';
import {extractFileNameFromYandex, getExperienceOptionByKey} from '../../utils/resume';
import {getResumeById} from '../../service/async-actions/async-actions-user';

export function ResumeReady() {
  const resume = useAppSelector((state) => state.user.resumeUser);

  return (
    <div>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Желаемая должность</ResumeFieldLabel>
        {
          resume?.desired_job &&
            <ResumeTitle>
              {resume?.desired_job}
            </ResumeTitle>
        }
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Резюме в формате PDF</ResumeFieldLabel>
        {
          resume?.document &&
            <ResumeTitle>
              {extractFileNameFromYandex(resume?.document)}
            </ResumeTitle>
        }
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Опыт работы</ResumeFieldLabel>
        {
          resume?.experience &&
            <ResumeTitle>
              {resume?.experience && getExperienceOptionByKey(resume.experience)}
            </ResumeTitle>
        }
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Ожидаемая зарплата</ResumeFieldLabel>
        <ResumeTitle>
          {resume?.desired_salary || '0'}&nbsp;₽
        </ResumeTitle>
      </ResumeFieldContainer>
      <ResumeFieldContainer>
        <ResumeFieldLabel>Мои компетенции</ResumeFieldLabel>
        <CompetencyList values={resume?.competencies || []} showDeleteButtons={false}/>
      </ResumeFieldContainer>
    </div>
  );
}