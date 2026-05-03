import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import App from "./app/App.tsx";
import GetStarted from "./app/GetStarted.tsx";
import Login from "./app/Login.tsx";
import LearnMore from "./app/LearnMore.tsx";
import Users from "./app/Users.tsx";
import Workouts from "./app/Workouts.tsx";
import Clubs from "./app/Clubs.tsx";
import ClubDetail from "./app/ClubDetail.tsx";
import CreateClub from "./app/CreateClub.tsx";
import NewWorkout from "./app/NewWorkout.tsx";
import Feed from "./app/Feed.tsx";
import Peers from "./app/Peers.tsx";
import PRs from "./app/PRs.tsx";
import BodyMetrics from "./app/BodyMetrics.tsx";
import Spotters from "./app/Spotters.tsx";
import Gyms from "./app/Gyms.tsx";
import FavoriteExercises from "./app/FavoriteExercises.tsx";
import Profile from "./app/Profile.tsx";
import ProfileEdit from "./app/ProfileEdit.tsx";
import UserProfile from "./app/UserProfile.tsx";
import SuggestedWorkout from "./app/SuggestedWorkout.tsx";
import ExerciseHistory from "./app/ExerciseHistory.tsx";
import { AppShell } from "./components/AppShell.tsx";
import { CurrentUserProvider } from "./context/CurrentUser.tsx";
import { ThemeProvider } from "./context/Theme.tsx";
import "./styles/index.css";
import Stats from "./app/Stats.tsx";


createRoot(document.getElementById("root")!).render(
  <ThemeProvider>
    <CurrentUserProvider>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/get-started" element={<GetStarted />} />
        <Route path="/login" element={<Login />} />
        <Route path="/learn-more" element={<LearnMore />} />
        <Route element={<AppShell />}>
          <Route path="/stats" element={<Stats />} />
          <Route path="/feed" element={<Feed />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/workouts/new" element={<NewWorkout />} />
          <Route path="/clubs" element={<Clubs />} />
          <Route path="/clubs/new" element={<CreateClub />} />
          <Route path="/clubs/:id" element={<ClubDetail />} />
          <Route path="/peers" element={<Peers />} />
          <Route path="/prs" element={<PRs />} />
          <Route path="/metrics" element={<BodyMetrics />} />
          <Route path="/spotters" element={<Spotters />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/profile/edit" element={<ProfileEdit />} />
          <Route path="/users" element={<Users />} />
          <Route path="/users/:id" element={<UserProfile />} />
          <Route path="/gyms" element={<Gyms />} />
          <Route path="/favorites" element={<FavoriteExercises />} />
          <Route path="/suggested-workout" element={<SuggestedWorkout />} />
          <Route path="/exercise-history" element={<ExerciseHistory />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </CurrentUserProvider>
  </ThemeProvider>,
);
