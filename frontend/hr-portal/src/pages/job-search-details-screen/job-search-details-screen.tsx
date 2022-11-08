import './job-search-details-screen.scss';
import {useAppSelector} from '../../app/hooks';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import moneyRUSIcon from '../../assets/img/job-seach/₽.svg';
import {ExpectedExperienceNameString} from '../../const';
import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import departmentLogoIcon from '../../assets/img/vacancy-card/departments-icon.svg';

function JobSearchDetailsScreen() {
  const vacancy = useAppSelector((state) => state.vacancy.vacancyByID);
  const vacancyExperience = ExpectedExperienceNameString[vacancy!.expected_experience as keyof typeof ExpectedExperienceNameString];

  return (
    <div className="jobSearchDetails-wrapper">
      <div className="jobSearchDetails-item jobSearchDetails-item__card">
        <div className="cardSide-item cardSide-item__criteria">
          <div className="name-vacancy">{vacancy?.name}</div>
          <div className="tabsInfo">
            {/*<div className="tabsItem">*/}
            {/*  <img src={publishedAtIcon} alt="publishedAtIcon"/>*/}
            {/*  <div className="tabs-text">{vacancy.published_at}</div>*/}
            {/*</div>*/}
            {(vacancy?.salary_to || vacancy?.salary_from) &&
            (
              <div className="tabsItem">
                <div className="tabs-image">
                  <img src={moneyIcon} alt="experience icon"/>
                </div>
                {
                  vacancy?.salary_to !== undefined && vacancy?.salary_from === undefined &&
                  (
                    <>
                      <div className="tabs-text">до {vacancy?.salary_to}</div>
                      <div className="tabs-image-rus">
                        <img src={moneyRUSIcon} alt="money rus icon"/>
                      </div>
                    </>
                  )
                }
                {
                  vacancy?.salary_to === undefined && vacancy?.salary_from !== undefined &&
                  (
                    <>
                      <div className="tabs-text">от {vacancy?.salary_from}</div>
                      <div className="tabs-image-rus">
                        <img src={moneyRUSIcon} alt="money rus icon"/>
                      </div>
                    </>
                  )
                }
                {
                  vacancy?.salary_to !== undefined && vacancy?.salary_from !== undefined &&
                  (<div className="tabs-text">
                    <div className="tabs-flex">
                      <div className="text">от {vacancy?.salary_from}</div>
                      <div className="tabs-image-rus">
                        <img src={moneyRUSIcon} alt="money rus icon"/>
                      </div>
                    </div>
                    <div className="tabs-flex">
                      <div className="text">до {vacancy?.salary_to}</div>
                      <div className="tabs-image-rus">
                        <img src={moneyRUSIcon} alt="money rus icon"/>
                      </div>
                    </div>
                  </div>)
                }
              </div>
            )
            }
            <div className="tabsItem">
              <div className="tabs-image">
                <img src={experienceIcon} alt="money icon"/>
              </div>
              <div className="tabs-text">
                {vacancyExperience}
              </div>
            </div>
          </div>
          <div className="navTabs">
            <button className="navTabs-btnItem navTabs-btnItem__respond">
              Откликнуться
            </button>
            <button className="navTabs-btnItem">
              <img src={likesIcon} alt="likes icon"/>
            </button>
          </div>
        </div>
        <div className="cardSide-item cardSide-item__departmentInfo">
          <div className="general-content">
            <div className="departmentInfo-header">
              <div className="tabsItem tabsItem__department">
                <div className="tabs-image">
                  <img src={departmentLogoIcon} alt="department Logo Icon"/>
                </div>
                <div className="tabs-text">
                  {vacancy?.department.name}
                </div>
              </div>
              <div className="name-departmentLeader">{vacancy?.department.leader.name} {vacancy?.department.leader.surname}</div>
            </div>
            <div className="departmentInfo-content">
              {vacancy?.department?.description}
            </div>
          </div>
          <div className="departmentInfo-viewAllVacancies navTabs">
            <button className="navTabs-btnItem navTabs-btnItem__department navTabs-btnItem__respond">
              Посмотреть вакансии
            </button>
          </div>
        </div>
      </div>
      <div className="jobSearchDetails-item jobSearchDetails-item__description">

      </div>
    </div>
  );
}

export default JobSearchDetailsScreen;