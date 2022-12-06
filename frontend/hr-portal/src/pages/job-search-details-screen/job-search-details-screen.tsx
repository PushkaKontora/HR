import './job-search-details-screen.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import {ExpectedExperienceNameString} from '../../const';
import likesIcon from '../../assets/img/vacancy-card/no_like.svg';
import departmentLogoIcon from '../../assets/img/vacancy-card/departments-icon.svg';
import UseEditor from '../../reused-components/text-editor/useEditor';
import TabsSalary from '../../components/tabs-salary/tabs-salary';
import {useEffect, useState} from 'react';
import TabsRespondEditVacancy from '../../components/tabs-respond-edit-vacancy/tabs-respond-edit-vacancy';
import {useParams} from 'react-router-dom';
import {getVacancyByID} from '../../service/async-actions/async-actions-vacancy';
import {UserStatus} from '../../types/user-status';
import ModalEditVacancy from '../../components/modal-edit-vacancy/modal-edit-vacancy';
import {refreshPageDetailsScreen} from '../../features/page/page-slice';

function JobSearchDetailsScreen() {
  const params = useParams();
  const prodId = params.id;
  const vacancy = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const refreshPage = useAppSelector((state) => state.page.isRefreshPageDetailsScreen);
  const vacancyExperience = ExpectedExperienceNameString[vacancy?.expected_experience as keyof typeof ExpectedExperienceNameString];
  const [convertedContent, setConvertedContent] = useState('');
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (prodId && vacancy === null) {
      dispatch(getVacancyByID(Number(prodId)));
      console.log('refreshed');
    }
  }, []);

  useEffect(() => {
    if (prodId && refreshPage) {
      console.log('refresh');
      dispatch(getVacancyByID(Number(prodId)));
      dispatch(refreshPageDetailsScreen(false));
    }
  }, [refreshPage]);


  useEffect(() => {
    if (vacancy && vacancy.description) {
      setConvertedContent(vacancy.description);
    } else {
      setConvertedContent('<p></p>');
    }
  }, [vacancy]);

  const createMarkup = (html: any) => {
    return UseEditor(html).fromHtml();
  };

  return (
    <>
      {
        user?.permission === UserStatus.employer
        && (<ModalEditVacancy/>)
      }
      <div className="jobSearchDetails-wrapper">
        <div className="jobSearchDetails-item jobSearchDetails-item__card">
          <div className="cardSide-item cardSide-item__criteria">
            <div className="name-vacancy">{vacancy?.name}</div>
            <div className="tabsInfo">
              <TabsSalary/>
              <div className="tabsItem">
                <div className="tabs-image">
                  <img src={experienceIcon} alt="money icon"/>
                </div>
                <div className="tabs-text">
                  {vacancyExperience}
                </div>
              </div>
            </div>
            <TabsRespondEditVacancy/>
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
        <div
          className="jobSearchDetails-item jobSearchDetails-item__description"
          dangerouslySetInnerHTML={createMarkup(convertedContent)}
        />
      </div>
    </>
  );
}

export default JobSearchDetailsScreen;