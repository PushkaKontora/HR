import './job-search-details-screen.scss';
import {useAppSelector} from '../../app/hooks';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import moneyRUSIcon from '../../assets/img/job-seach/₽.svg';
import {ExpectedExperienceNameString} from '../../const';
import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import departmentLogoIcon from '../../assets/img/vacancy-card/departments-icon.svg';
import UseEditor from '../../reused-components/text-editor/useEditor';

function JobSearchDetailsScreen() {
  const vacancy = useAppSelector((state) => state.vacancy.vacancyByID);
  const vacancyExperience = ExpectedExperienceNameString[vacancy?.expected_experience as keyof typeof ExpectedExperienceNameString];

  const editorApi = UseEditor('<p><b>Описание вакансии</b>\n At Emerson, we are innovators and problem-solvers, focused on a common purpose: leaving our world in a better place than we found it. Each and every day, our foundational valuesintegrity, safety and quality, supporting our people, customer focus, continuous improvement, collaboration and innovationinform every decision we make and empower our employees to keep reaching higher. As a global technology and engineering leader, we provide groundbreaking solutions for customers in industrial, commercial, and residential' +
    ' markets. Our Emerson Automation Solutions business helps process, hybrid, and discrete manufacturers maximize production and protect personnel and the environment while optimizing their energy and operating costs. Our Emerson Commercial & Residential Solutions business helps ensure human comfort and health, protect food quality and safety, advance energy efficiency and create sustainable infrastructure.\n' +
    '\n' +
    'Emerson, a Fortune 500 company with $15.3 billion in sales and 200 manufacturing locations worldwide, is committed to helping employees grow and thrive throughout their careers.\n' +
    'Whether youre an established professional looking for a career change, an undergraduate student exploring options or a recent MBA graduate, youll find a variety of opportunities at Emerson. Join our team and start your journey today.\n' +
    '\n' +
    'Emerson Automation Solutions in Austin, Texas is looking for a versatile Senior Software Quality Assurance Engineer to become a member of the System Integration and Quality team responsible for ensuring new feature development results in a high-quality offering to our customers.In this role, you will be working within a Scaled Agile Framework (SAFe)-based organization dedicated to delivering the highest quality, world-class process control products built across web, cloud, PC, and embedded platforms integrated with locally developed hardware.The successful candidate should be able to work in a dynamic and fast-paced environment and communicate effectively with a wide range of people, experience levels, and technical backgrounds.\n</p>');

  return (
    <div className="jobSearchDetails-wrapper">
      <div className="jobSearchDetails-item jobSearchDetails-item__card">
        <div className="cardSide-item cardSide-item__criteria">
          <div className="name-vacancy">{vacancy?.name}</div>
          <div className="tabsInfo">
            {(vacancy?.salary_to || vacancy?.salary_from) &&
            (
              <div className="tabsItem">
                <div className="tabs-image">
                  <img src={moneyIcon} alt="experience icon"/>
                </div>
                {
                  vacancy?.salary_to !== null && vacancy?.salary_from === null &&
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
                  vacancy?.salary_to === null && vacancy?.salary_from !== null &&
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
                  vacancy?.salary_to !== null && vacancy?.salary_from !== null &&
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
      <div className="jobSearchDetails-item jobSearchDetails-item__description" dangerouslySetInnerHTML={editorApi.fromHtml()}>

      </div>
    </div>
  );
}

export default JobSearchDetailsScreen;