import './job-search-details-screen.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import {ExpectedExperienceNameString} from '../../const';
import departmentLogoIcon from '../../assets/img/vacancy-card/departments-icon.svg';
import UseEditor from '../../reused-components/text-editor/useEditor';
import TabsSalary from '../../components/tabs-salary/tabs-salary';
import {useEffect, useState} from 'react';
import TabsRespondEditVacancy from '../../components/tabs-respond-edit-vacancy/tabs-respond-edit-vacancy';
import {Link, useParams} from 'react-router-dom';
import {
  getLastVacancyRequest,
  getVacancyByID,
  getVacancyWishlist,
  VacancyWishListSortBy
} from '../../service/async-actions/async-actions-vacancy';
import {UserStatus} from '../../types/user-status';
import ModalEditVacancy from '../../components/modal-edit-vacancy/modal-edit-vacancy';
import {refreshPageDetailsScreen} from '../../features/page/page-slice';
import clockIcon from '../../assets/img/vacancy-card/clock.svg';
import {getBackTimestampRussian} from '../../utils/times';
import ModalRespondRequest from '../../components/modal-respond-request/modal-respond-request';

function JobSearchDetailsScreen() {
  const params = useParams();
  const prodId = params.id;
  const vacancy = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const refreshPage = useAppSelector((state) => state.page.isRefreshPageDetailsScreen);
  const requestDate = useAppSelector((state) => state.vacancy.requestDate);
  const vacancyExperience = ExpectedExperienceNameString[vacancy?.expected_experience as keyof typeof ExpectedExperienceNameString];
  const [convertedContent, setConvertedContent] = useState('');
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (prodId && vacancy === null) {
      dispatch(getVacancyByID(Number(prodId)));
      dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));
    }
  }, []);

  useEffect(() => {
    if (prodId && refreshPage) {
      dispatch(getVacancyByID(Number(prodId)));
      dispatch(refreshPageDetailsScreen(false));
    }
  }, [refreshPage]);


  useEffect(() => {
    if (vacancy) {
      dispatch(getLastVacancyRequest(vacancy.id));
    }

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
      <ModalRespondRequest/>

      <div className="jobSearchDetails-wrapper">
        <div className="jobSearchDetails-item jobSearchDetails-item__card">
          <div className="cardSide-item cardSide-item__criteria">
            <div className="cardSide-header">
              <div className="name-vacancy">{vacancy?.name}</div>
              {
                requestDate &&
                  <div className='cardSide-item__requestDate'>
                    Отклик отправлен&nbsp;
                    {(new Date(requestDate)).toLocaleDateString(undefined, {day: 'numeric', year: 'numeric', month: 'numeric'})}
                  </div>
              }
            </div>
            <div className="tabsInfo">

              <div className="tabsItem">
                <div className="tabs-image">
                  <img src={clockIcon} alt="created"/>
                </div>
                <div className="tabs-text">
                  {getBackTimestampRussian(vacancy?.published_at)}
                </div>
              </div>

              <TabsSalary salary_from={vacancy?.salary_from} salary_to={vacancy?.salary_to} />

              <div className="tabsItem">
                <div className="tabs-image">
                  <img src={experienceIcon} alt="experience"/>
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
              <Link to={'/'} className="navTabs-btnItem navTabs-btnItem__department navTabs-btnItem__respond">
                Посмотреть вакансии
              </Link>
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