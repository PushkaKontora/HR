import {createSlice} from '@reduxjs/toolkit';
import {ButtonVacancyCard, TabInHeader} from '../../const';

interface PageSlice {
  buttonVacancyCard: ButtonVacancyCard;
  activeTabInHeader: TabInHeader | null;
  isRefreshPageDetailsScreen: boolean;
}

const initialState: PageSlice = {
  buttonVacancyCard: ButtonVacancyCard.vacancies,
  activeTabInHeader: TabInHeader.vacancies,
  isRefreshPageDetailsScreen: false
};

const pageSlice = createSlice({
  name: 'page',
  initialState,
  reducers: {
    changeButtonVacancyCard(state, action) {
      state.buttonVacancyCard = action.payload;
    },
    changeActiveTabInHeader(state, action) {
      state.activeTabInHeader = action.payload;
    },
    refreshPageDetailsScreen(state, action) {
      state.isRefreshPageDetailsScreen = action.payload;
    }
  }
});

export const {
  changeButtonVacancyCard,
  changeActiveTabInHeader,
  refreshPageDetailsScreen,
} = pageSlice.actions;

export default pageSlice.reducer;