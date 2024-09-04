// import { StyleSheet,  } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { useFonts } from "expo-font";
import { RootStoreContext } from "./store/store_context";
import RootStore from "./store/root_store";

import BottomMenu from "./components/bottom_menu";

const Stack = createNativeStackNavigator();

export default function App() {
  const [fontsLoaded] = useFonts({
    DelaGothicOneRegular: require("./assets/fonts/DelaGothicOne-Regular.ttf"),
    ManropeBold: require("./assets/fonts/Manrope-Bold.ttf"), //700
    ManropeExtraLight: require("./assets/fonts/Manrope-ExtraLight.ttf"), //200
    ManropeRegular: require("./assets/fonts/Manrope-Regular.ttf"),
    ManropeSemiBold: require("./assets/fonts/Manrope-SemiBold.ttf"), //600
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
              <Stack.Screen name="MainScreen" component={MainScreen} />
              <Stack.Screen name="BottomMenu" component={BottomMenu} />
            </Stack.Navigator>
            <BottomMenu />
          </>
        )}
      </RootStoreContext.Provider>
    </NavigationContainer>
  );
}
