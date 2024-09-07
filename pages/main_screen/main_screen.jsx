import {
  StyleSheet,
  View,
  StatusBar,
  SafeAreaView,
  ScrollView,
  Button,
  FlatList,
  Text,
  Modal,
} from "react-native";
import Header from "../../components/header";
import MiniProfileInfo from "../../components/mini_profile_info";
import AboutFund from "../../components/about_fund";
import FundCard from "../../components/fund_card";
import FilterButton from "../../components/filter_button";

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
        <View style={[styles.component, styles.filterButtons]}>
          <FilterButton />
        </View>
        <View style={[styles.component, styles.funds]}>
          <FundCard />
          <FundCard collect_sum={50000} name="Помощь детям" />
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
  filterButtons: {
    marginTop: 20,
  },
  funds: {
    marginTop: 5,
    gap: 15,
    marginBottom: 80,
  },
});

export default MainScreen;
