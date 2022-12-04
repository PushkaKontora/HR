import likesIcon from '../../assets/img/vacancy-card/no_like.svg';
import './resume-card.scss';
import {ResumeUser} from '../../types/resume';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import placeholder from '../../assets/svg/placeholder.svg';
import {extractFileNameFromYandex, getExperienceOptionByKey} from '../../utils/resume';
import {Icon, UserIcon, ResumeField} from './styled';
import {ResumeTitle} from '../styled/resume/resume-title';
import {LoadButton} from '../../reused-components/load-button/load-button';

type VacancyCard = {
  resume: ResumeUser
}

function ResumeCard({resume}: VacancyCard) {
  const handleClickVacancyCard = () => {
    //dispatch(setVacancyByID(vacancy));
    //navigate(`${NoAuthRoutes.Vacancy}/${vacancy.id}`);
  };

  const handlerClickRespond = (e: any) => {
    //dispatch(setVacancyByID(vacancy));
    //e.stopPropagation()
    //dispatch(setStateRespondModal(true));
  };

  return (
    <div className="resumeCardWrapper" onClick={handleClickVacancyCard}>
      <div className='resumeCardBg'>
        <div className="resumeCardItem resumeCardItem__content">
          <div className="resumeCardInfo resumeCardInfo__title">
            {resume.desired_job}
          </div>
          <div className="resumeCardInfo resumeCardInfo__description">
            <ResumeField>
              <Icon src={experienceIcon}/>
              {getExperienceOptionByKey(resume.experience)}
            </ResumeField>
            {
              resume.desired_salary &&
                <ResumeField>
                  <Icon src={moneyIcon}/>
                  {resume.desired_salary} ₽
                </ResumeField>
            }
          </div>
          <div className="resumeCardInfo resumeCardInfo__tabs">
            {resume.competencies.map((item, idx) => {
              return (
                <div key={idx} className="tabsItem">
                  {item}
                </div>);
            })}
          </div>
        </div>
        <UserIcon src={resume.owner.photo || placeholder}/>
      </div>
      <div className="resumeCardItem resumeCardItem__action">
        <div className='resumeDownload'>
          <ResumeTitle bgColor={'#fff'}>
            {extractFileNameFromYandex(resume.document)}
          </ResumeTitle>
          <a href={resume?.document} download>
            <LoadButton bgColor={'#fff'} onClick={() => {return;}}/>
          </a>
        </div>

        <div className="actionItem navTabs">
          <button className="navTabs-btnItem">
            <img src={likesIcon} alt="likes icon"/>
          </button>
          <button
            className="navTabs-btnItem navTabs-btnItem__respond"
            onClick={handlerClickRespond}
          >
            Показать контакты
          </button>
        </div>
      </div>
    </div>
  );
}

export default ResumeCard;