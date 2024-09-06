import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useFonts } from "expo-font";
import { RootStoreContext } from "./store/store_context";
import RootStore from "./store/root_store";

import BottomMenu from "./components/bottom_menu";
import MainScreen from "./pages/main_screen/main_screen";
import ProfileScreen from "./pages/profile_screen/profile_screen";
import AboutFundScreen from "./pages/about_fund_screen/about_fund_screen";

const Stack = createNativeStackNavigator();

export default function App() {
  const [fontsLoaded] = useFonts({
    IBMRegular: require("./assets/fonts/IBMPlexSans-Regular.ttf"), //400
    IBMMedium: require("./assets/fonts/IBMPlexSans-Medium.ttf"), //500
    IBMSemiBold: require("./assets/fonts/IBMPlexSans-SemiBold.ttf"), //600
  });
  return (
    <NavigationContainer>
      <RootStoreContext.Provider value={new RootStore()}>
        {fontsLoaded && (
          <>
            <Stack.Navigator
              initialRouteName="MainScreen"
              screenOptions={{ headerShown: false }}
            >
              <Stack.Screen name="ProfileScreen" component={ProfileScreen} />
              <Stack.Screen name="MainScreen" component={MainScreen} />
              <Stack.Screen
                name="AboutFundScreen"
                component={AboutFundScreen}
              />
              {/* <Stack.Screen name="BottomMenu" component={BottomMenu} /> */}
            </Stack.Navigator>
            <BottomMenu />
          </>
        )}
      </RootStoreContext.Provider>
    </NavigationContainer>
  );
}
