import {
  Image,
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { SvgXml } from "react-native-svg";
import { useNavigation } from "@react-navigation/native";

import ModalFund from "../../components/modal_fund";

import { arrowBack, clockIcon, peopleIcon } from "../../images/images";

const AboutFundScreen = ({
  uri = "https://legacy.reactjs.org/logo-og.png",
  name = "Ремонт дома для пожилой пары",
  collect_sum = 30000,
  full_sum = 100000,
  countPeople = 7162,
  time = "5 дней",
}) => {
  const navigation = useNavigation();
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" />

      <ScrollView>
        <View style={[styles.component, styles.fundInfo]}>
          <Image
            source={{ uri: uri }}
            height={240}
            width={"100%"}
            style={styles.mainImage}
          />
          <TouchableOpacity
            style={styles.arrowBackButton}
            onPress={() => {
              navigation.goBack();
            }}
          >
            <SvgXml xml={arrowBack} />
          </TouchableOpacity>
          <View style={styles.mainInfo}>
            <Text style={styles.nameText}>{name}</Text>
            <View style={styles.statusNames}>
              <Text style={styles.statusNameText}>Собрано</Text>
              <Text style={styles.statusNameText}>Нужно собрать</Text>
            </View>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFillBar,
                  { width: `${(collect_sum / full_sum) * 100}%` },
                ]}
              />
            </View>
            <View style={styles.progressSum}>
              <Text style={styles.sumText}>
                {collect_sum.toLocaleString("ru")} ₽
              </Text>
              <Text style={styles.sumText}>
                {full_sum.toLocaleString("ru")} ₽
              </Text>
            </View>
            <View style={styles.statsViews}>
              <View style={styles.statsView}>
                <SvgXml xml={peopleIcon} />
                <Text style={styles.statsText}>{countPeople}</Text>
              </View>
              <View style={styles.statsView}>
                <SvgXml xml={clockIcon} />
                <Text style={styles.statsText}>{time}</Text>
              </View>
            </View>
            <View style={styles.helpButton}>
              <ModalFund width={"100%"} />
            </View>
          </View>
        </View>
        <View style={[styles.component, styles.aboutFund]}>
          <Text style={styles.aboutFundText}>О сборе</Text>
          <Text style={styles.mainFundText}>
            Это инициатива, направленная на помощь Николаю и Валентине Ивановым
            - пожилой паре, которая вот уже многие годы разделяет свою жизнь,
            радости и трудности под одной крышей. Николай и Валентина Ивановы -
            это не только имя и фамилия, но и символ преданности, тепла и
            семейного счастья. Они прожили вместе столько лет, что их дом стал
            свидетелем всех их радостей и печалей, моментов счастья и испытаний.
            Сейчас, когда они стареют, их дом требует заботы и внимания.
          </Text>
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
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 0,
      height: 0,
    },
    shadowOpacity: 1,
    shadowRadius: 8,
  },
  fundInfo: {
    marginTop: 20,
    marginHorizontal: 20,
  },
  mainInfo: {
    padding: 20,
    marginTop: 15,
  },
  mainImage: {
    objectFit: "cover",
    borderTopRightRadius: 20,
    borderTopLeftRadius: 20,
  },
  nameText: {
    color: "rgba(22, 3, 111, 1)",
    fontFamily: "IBMSemiBold",
    fontSize: 18,
  },
  progressBar: {
    width: "100%",
    height: 5,
    marginTop: 10,
    backgroundColor: "rgba(70, 47, 181, 0.3)",
    borderRadius: 3,
    position: "relative",
  },
  progressFillBar: {
    backgroundColor: "rgba(22, 3, 111, 1)",
    position: "absolute",
    left: 0,
    top: 0,
    height: 5,
    borderRadius: 3,
  },
  statusNames: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 15,
  },
  statusNameText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
  },
  sumText: {
    fontFamily: "IBMMedium",
    color: "rgba(52, 52, 52, 1)",
  },
  progressSum: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
  },
  statsViews: {
    flexDirection: "row",
    marginTop: 15,
    gap: 5,
  },
  statsView: {
    flexDirection: "row",
    backgroundColor: "rgba(237, 236, 240, 1)",
    height: 30,
    width: "50%",
    borderRadius: 7,
    justifyContent: "center",
    alignItems: "center",
    gap: 10,
  },
  statsText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
  },
  helpButton: {
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
    height: 35,
    backgroundColor: "rgba(48, 31, 129, 1)",
    borderRadius: 10,
    marginTop: 15,
  },
  helpButtonText: {
    color: "white",
    fontFamily: "IBMSemiBold",
  },
  aboutFund: {
    marginTop: 20,
    marginHorizontal: 20,
    padding: 20,
    marginBottom: 100,
  },
  aboutFundText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
    fontSize: 16,
  },
  mainFundText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMRegular",
    marginTop: 5,
  },
  arrowBackButton: {
    position: "absolute",
    backgroundColor: "rgba(255, 255, 255, 1)",
    justifyContent: "center",
    alignItems: "center",
    width: 32,
    height: 32,
    borderRadius: 10,
    left: 20,
    top: 20,
  },
});
export default AboutFundScreen;
