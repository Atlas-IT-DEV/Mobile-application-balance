import {
  StyleSheet,
  View,
  StatusBar,
  SafeAreaView,
  ScrollView,
} from "react-native";
import Header from "../../components/header";
import MiniProfileInfo from "../../components/mini_profile_info";
import AboutFund from "../../components/about_fund";

const MainScreen = () => {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />
      <ScrollView>
        <View style={styles.header}>
          <Header />
        </View>
        <View style={[styles.profile, styles.component]}>
          <MiniProfileInfo />
        </View>
        <View style={[styles.component, styles.aboutFund]}>
          <AboutFund />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    width: "100%",
    height: "100%",
  },

  component: {
    paddingHorizontal: 20,
  },
  header: {
    paddingHorizontal: 38,
    marginTop: 15,
  },
  profile: {
    marginTop: 20,
  },
  aboutFund: {
    marginTop: 15,
  },
});

export default MainScreen;
